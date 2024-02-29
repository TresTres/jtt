from typing import Optional

from tree_tools.src import jtt_tree
from tree_tools.src.jtt_query import operations


class NodeQueryError(Exception):
    """
    Handle errors in query processing.
    """

    pass

class Cursor: 
    """
    This class is used to represent the current position in the tree during query processing.
    """
    node: Optional[jtt_tree.TreeNode]
    
    def __init__(self) -> None:
        self.node = None
        
        
    def visit(self, node: jtt_tree.TreeNode) -> None:
        """
        Move the cursor to the specified node.
        
        Args:
            node: The TreeNode to move the cursor to.
        """
        self.node = node


class QueryProcessor:
    """
    This class is used to evaluate queries against TreeNode objects.
    """
    operation_chain: operations.QueryOperationChain
    result_tree: jtt_tree.TreeNode
    read_tree: jtt_tree.TreeNode
    cursor: Cursor
    
    def __init__(self, tree: jtt_tree.TreeNode, operation_chain: operations.QueryOperationChain) -> None:
        self.read_tree = tree
        self.result_tree = None
        self.operation_chain = operation_chain
        self.cursor = Cursor()
        self.cursor.visit(self.read_tree)
    
    def execute(self) -> jtt_tree.TreeNode:
        """
        Execute the query operations and store the result in the result_tree attribute.
        """
        for operation in self.operation_chain:
            self.cursor.visit(operation.perform(self.cursor.node))
            if not self.cursor.node:
                self.result_tree = jtt_tree.NullTreeNode()
                return self.result_tree
            
        self.result_tree = self.cursor.node
        return self.result_tree



