import enum
import typing
import reprlib


class NodeType(enum.Enum):
    NULL = "NULL"
    STRING = "STRING"
    NUMBER = "NUMBER"
    ARRAY = "ARRAY"
    OBJECT = "OBJECT"
    BOOLEAN = "BOOLEAN"


NodeValue = typing.Union[
    None, str, int, float, typing.List["TreeNode"], typing.Dict[str, "TreeNode"]
]


class TreeNode:

    """
    Node representing data from the JSON tree, with the data boxed in a value field.
    Each node maintains the following metadata:
    - type of data contained
    - number of total descendants in the tree
    """

    type: NodeType
    value: NodeValue
    descendant_count: int
    repr_object = reprlib.Repr()
    repr_object.maxarray = 6
    repr_object.maxstring = 80
    repr_object.maxlong = 80
    repr_object.maxother = 80

    def __repr__(self) -> str:
        return TreeNode.repr_object.repr(self.value)


class NullTreeNode(TreeNode):
    type = NodeType.NULL

    def __init__(self):
        self.value = None
        self.descendant_count = 0


class StringTreeNode(TreeNode):
    type = NodeType.STRING

    def __init__(self, value: str):
        self.value = value
        self.descendant_count = 0


class NumberTreeNode(TreeNode):
    type = NodeType.NUMBER

    def __init__(self, value: typing.Union[int, float]):
        self.value = value
        self.descendant_count = 0


class BooleanTreeNode(TreeNode):
    type = NodeType.BOOLEAN

    def __init__(self, value: bool):
        self.value = value
        self.descendant_count = 0

class ListTreeNode(TreeNode):
    type = NodeType.ARRAY

    def __init__(self, value: typing.List[TreeNode]):
        self.value = []
        self.descendant_count = 0
        for v in value:
            if v is None:
                self.value.append(NullTreeNode())
            elif type(v) == str:
                self.value.append(StringTreeNode(v))
            elif type(v) == int or type(v) == float:
                self.value.append(NumberTreeNode(v))
            elif type(v) == bool:
                self.value.append(BooleanTreeNode(v))
            elif type(v) == dict:
                self.value.append(ObjectTreeNode(v))
            elif type(v) == list:
                self.value.append(ListTreeNode(v))
            else:
                raise TypeError(f"Invalid type: {type(v)} for value {v}")
            self.descendant_count += self.value[-1].descendant_count + 1


class ObjectTreeNode(TreeNode):
    type = NodeType.OBJECT

    def __init__(self, value: typing.Dict[str, TreeNode]):
        self.value = {}
        self.descendant_count = 0
        for k, v in value.items():
            if v is None:
                self.value[k] = NullTreeNode()
            elif type(v) == str:
                self.value[k] = StringTreeNode(v)
            elif type(v) == int or type(v) == float:
                self.value[k] = NumberTreeNode(v)
            elif type(v) == bool:
                self.value[k] = BooleanTreeNode(v)
            elif type(v) == dict:
                self.value[k] = ObjectTreeNode(v)
            elif type(v) == list:
                self.value[k] = ListTreeNode(v)
            else:
                raise TypeError(f"Invalid type: {type(v)} for value {v}")
            self.descendant_count += self.value[k].descendant_count + 1


def create_tree(data: typing.Dict[str, typing.Any]) -> ObjectTreeNode:
    if type(data) != dict:
        raise ValueError(f"Invalid type: {type(data)} for value {data}")
    return ObjectTreeNode(data)
