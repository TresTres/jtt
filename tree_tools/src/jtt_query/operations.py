import typing

from tree_tools.src import jtt_tree
from tree_tools.src.jtt_query import utils


class QueryOperationError(Exception):
    pass


class QueryOperation:
    strict: bool

    def __init__(self, strict: bool = False) -> None:
        self.strict = strict
        pass

    def evaluate(self, node: jtt_tree.TreeNode) -> typing.List[jtt_tree.TreeNode]:
        pass


class GetAll(QueryOperation):
    """
    Get all child nodes.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def evaluate(self, node: jtt_tree.TreeNode) -> typing.List[jtt_tree.TreeNode]:
        if node.type is jtt_tree.NodeType.ARRAY:
            return node.value
        if node.type is jtt_tree.NodeType.OBJECT:
            return list(node.value.values())
        if self.strict:
            raise QueryOperationError(
                "Cannot evaluate query get-all operation on non-array or non-object node."
            )
        return []


class FilterIndex(QueryOperation):

    """
    Filter child nodes by index.
    """

    index: int

    def __init__(self, index: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.index = index

    def evaluate(self, node: jtt_tree.TreeNode) -> typing.List[jtt_tree.TreeNode]:
        if node.type is jtt_tree.NodeType.ARRAY:
            if utils.index_within_list(self.index, node.value):
                return [node.value[self.index]]
            if self.strict:
                raise QueryOperationError(
                    f"Index {self.index} out of bounds for array node with length {len(node.value)}."
                )
            return []
        if self.strict:
            raise QueryOperationError(
                "Cannot evaluate query index-matching operation on non-array node."
            )
        return []


class FilterKey(QueryOperation):
    predicate: str

    def __init__(self, predicate: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.predicate = predicate

    def evaluate(self, node: jtt_tree.TreeNode) -> typing.List[jtt_tree.TreeNode]:
        if node.type is jtt_tree.NodeType.OBJECT:
            if self.predicate in node.value:
                return [node.value[self.predicate]]
            if self.strict:
                raise QueryOperationError(
                    f"Key {self.predicate} not found in object node with keys {node.value.keys()}."
                )
            return []
        if self.strict:
            raise QueryOperationError(
                "Cannot evaluate query key-matching operation on non-object node."
            )
        return []
