import math
import enum
import typing
import reprlib



class NodeType(enum.Enum):
    STRING = "STRING"
    INT = "INT"
    ARRAY = "ARRAY"
    OBJECT = "OBJECT"

NodeValue = typing.Union[str, int, typing.List["TreeNode"], typing.Dict[str, "TreeNode"]]

class TreeNode:
    type: NodeType
    value: NodeValue
    repr_object = reprlib.Repr()    
    blob_str = "**"
    
    def __repr__(self) -> str:
        return TreeNode.repr_object.repr(self.value)
    
    def accept_visitor(self, visitor: 'NodeVisitor') -> None:
        pass 

class StringTreeNode(TreeNode):
    type = NodeType.STRING

    def __init__(self, value: str):
        self.value = value

    def accept_visitor(self, visitor: 'NodeVisitor') -> None:
        visitor.visit_string_node(self)


class IntTreeNode(TreeNode):
    type = NodeType.INT

    def __init__(self, value: int):
        self.value = value

    def accept_visitor(self, visitor: 'NodeVisitor') -> None:
        visitor.visit_int_node(self)


class ListTreeNode(TreeNode):
    type = NodeType.ARRAY

    def __init__(self, value: typing.List[TreeNode]):
        self.value = []
        for v in value:
            if type(v) == str:
                self.value.append(StringTreeNode(v))
            elif type(v) == int:
                self.value.append(IntTreeNode(v))
            elif type(v) == dict:
                self.value.append(ObjectTreeNode(v))
            elif type(v) == list:
                self.value.append(ListTreeNode(v))
            else:
                raise TypeError(f"Invalid type: {type(v)} for value {v}")
            
    def accept_visitor(self, visitor: 'NodeVisitor') -> None:
        visitor.visit_array_node(self)

class ObjectTreeNode(TreeNode):
    type = NodeType.OBJECT

    def __init__(self, value: typing.Dict[str, TreeNode]):
        self.value = {}
        for k, v in value.items():
            if type(v) == str:
                self.value[k] = StringTreeNode(v)
            elif type(v) == int:
                self.value[k] = IntTreeNode(v)
            elif type(v) == dict:
                self.value[k] = ObjectTreeNode(v)
            elif type(v) == list:
                self.value[k] = ListTreeNode(v)
            else:
                raise TypeError(f"Invalid type: {type(v)} for value {v}")
            
    def accept_visitor(self, visitor: 'NodeVisitor') -> None:
        visitor.visit_object_node(self)
            


def create_tree(data: typing.Dict[str, typing.Any]) -> ObjectTreeNode:
    if type(data) != dict:
        raise ValueError(f"Invalid type: {type(data)} for value {data}")
    return ObjectTreeNode(data)


def search_tree_keys(
    tree: ObjectTreeNode, path: typing.List[str]
) -> typing.List[TreeNode]:
    return tree.collect_path_matches(path)
