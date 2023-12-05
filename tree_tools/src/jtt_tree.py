import math
import enum
import typing
import reprlib


class NodeType(enum.Enum):
    STRING = "STRING"
    INT = "INT"
    ARRAY = "ARRAY"
    OBJECT = "OBJECT"


class TreeNode:
    type: NodeType
    value: typing.Union[str, int, typing.List["TreeNode"], typing.Dict[str, "TreeNode"]]
    repr_object = reprlib.Repr()    
    blob_str = "**"
    
    def __repr__(self) -> str:
        return TreeNode.repr_object.repr(self.value)

    def collect_path_matches(self, path: typing.List[str]) -> typing.List["TreeNode"]:
        """
        Collects all nodes that match the target path.
        """
        pass


    

class StringTreeNode(TreeNode):
    type = NodeType.STRING

    def __init__(self, value: str):
        self.value = value

    def collect_path_matches(self, _path: typing.List[str]) -> typing.List[TreeNode]:
        """
        No key on this class
        """
        return [self]


class IntTreeNode(TreeNode):
    type = NodeType.INT

    def __init__(self, value: int):
        self.value = value

    def collect_path_matches(self, _path: typing.List[str]) -> typing.List[TreeNode]:
        """
        No key on this class
        """
        return [self]


class ListTreeNode(TreeNode):
    type = NodeType.ARRAY

    def __init__(self, value: typing.List[typing.Any]):
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

    def collect_path_matches(self, path: typing.List[str]) -> typing.List[TreeNode]:
        """
        Collects all nodes that match the target path.
        Recurse down on children with a matching index.
        """
        if len(path) == 0:
            return [self]
        term = path.pop(0)
        index = -math.inf
        if term.isdigit():
            index = int(term)
        elif term != self.blob_str:
            return []
        matching = []
        for ind, node in enumerate(self.value):
            if ind == index or term == self.blob_str:
                matching.extend(node.collect_path_matches(path.copy()))
        return matching

class ObjectTreeNode(TreeNode):
    type = NodeType.OBJECT

    def __init__(self, value: typing.Dict[str, typing.Any]):
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
            

    def collect_path_matches(self, path: typing.List[str]) -> typing.List[TreeNode]:
        """
        Collects all nodes that match the target path.
        Recurses down on children with a matching key.
        """
        if len(path) == 0:
            return [self]
        term = path.pop(0)
        matching = []
        for k, v in self.value.items():
            if k == term or term == self.blob_str:
                matching.extend(v.collect_path_matches(path.copy()))
        return matching


def create_tree(data: typing.Dict[str, typing.Any]) -> ObjectTreeNode:
    if type(data) != dict:
        raise ValueError(f"Invalid type: {type(data)} for value {data}")
    return ObjectTreeNode(data)


def search_tree_keys(
    tree: ObjectTreeNode, path: typing.List[str]
) -> typing.List[TreeNode]:
    return tree.collect_path_matches(path)
