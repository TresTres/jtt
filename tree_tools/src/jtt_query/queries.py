import typing
from collections import deque

from tree_tools.src import jtt_tree
from tree_tools.src.jtt_query import operations


class NodeQueryError(Exception):
    """
    Handle errors in query processing.
    """

    pass


class NodeQuery(jtt_tree.NodeVisitor):

    """
    This class is used to build and evaluate queries against TreeNode objects.
    """

    op_queue: typing.Deque[operations.QueryOperation]
    tree: jtt_tree.TreeNode
    results: typing.List[jtt_tree.TreeNode]

    def __init__(self, tree: jtt_tree.TreeNode) -> None:
        self.tree = tree
        self.op_queue = deque()
        self.results = []
    

    def _process_op(self, node: jtt_tree.TreeNode) -> typing.List[jtt_tree.TreeNode]:
        """
        Process the next query operation.
        """
        if not self.op_queue:
            raise NodeQueryError("Nothing left to evaluate, query path is empty.")
        query_op = self.op_queue.popleft()
        return query_op.evaluate(node)
    
    def collect_results(self) -> typing.List[jtt_tree.TreeNode]:
        """
        Collect the results of the query by triggering the visitation.
        """
        self.tree.accept_visitor(self)
        return self.results

    def copy_query_to_new_node(self, node: jtt_tree.TreeNode) -> "NodeQuery":
        """
        Copy the query to a new node with the same operations.
        """
        new_query = NodeQuery(node)
        new_query.op_queue = self.op_queue.copy()
        return new_query


    def visit_null_node(self, node: jtt_tree.NullTreeNode) -> None:
        """
        Add the node to the results if the path is empty.
        Otherwise, evaluate according to the query.
        """
        if not self.op_queue:
            self.results.append(node)
            return
        self.results.extend(self._process_op(node))

    def visit_string_node(self, node: jtt_tree.StringTreeNode) -> None:
        """
        Add the node to the results if the path is empty.
        Otherwise, evaluate according to the query.
        """
        if not self.op_queue:
            self.results.append(node)
            return
        self.results.extend(self._process_op(node))

    def visit_number_node(self, node: jtt_tree.NumberTreeNode) -> None:
        """
        Add the node to the results if the path is empty.
        Otherwise, evaluate according to the query.
        """
        if not self.op_queue:
            self.results.append(node)
            return
        self.results.extend(self._process_op(node))

    def visit_boolean_node(self, node: jtt_tree.BooleanTreeNode) -> None:
        """
        Add the node to the results if the path is empty.
        Otherwise, evaluate according to the query.
        """
        if not self.op_queue:
            self.results.append(node)
            return
        self.results.extend(self._process_op(node))

    def visit_array_node(self, node: jtt_tree.ListTreeNode) -> None:
        """
        Add the node to the results if the path is empty.
        Otherwise, evaluate according to the query, and then recurse on each result.
        """
        if not self.op_queue:
            self.results.append(node)
            return
        for child in self._process_op(node):
            new_query = self.copy_query_to_new_node(child)
            self.results.extend(new_query.collect_results())


    def visit_object_node(self, node: jtt_tree.ObjectTreeNode) -> None:
        """
        Add the node to the results if the path is empty.
        Otherwise, evaluate according to the query, and then recurse on each result.
        """
        if not self.op_queue:
            self.results.append(node)
            return
        for child in self._process_op(node):
            new_query = self.copy_query_to_new_node(child)
            self.results.extend(new_query.collect_results())
        



class TreeQuery(NodeQuery):

    """
    This class is used to build and evaluate queries against JSON objects.
    """

    def filter_key(self, predicate: str, strict: bool = False) -> 'TreeQuery':
        self.op_queue.append(operations.FilterKey(predicate, strict=strict))
        return self

    def filter_index(self, index: int, strict: bool = False) -> 'TreeQuery':
        self.op_queue.append(operations.FilterIndex(index, strict=strict))
        return self

    def get_all(self, strict: bool = False) -> 'TreeQuery':
        self.op_queue.append(operations.GetAll(strict=strict))
        return self
