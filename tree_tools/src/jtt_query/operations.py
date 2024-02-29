from abc import abstractmethod
from typing import Optional

from tree_tools.src import jtt_tree
from tree_tools.src.jtt_query import utils


class QueryOperationError(Exception):
    pass


class QueryOperation: 
    """
    Represents a single operation in an operation chain. 
    """
    
    next: Optional['QueryOperation']
    
    @abstractmethod
    def perform(self, node: jtt_tree.TreeNode) -> Optional[jtt_tree.TreeNode]:
        """
        Conducts an operation on a node and returns a result if possible.
        An operation
        """
        pass

    
class KeyOperation(QueryOperation):
    """
    This class is used to represent the key selection in a query.  
    Key selection only applies to ObjectTreeNodes and returns the node at the specified key.
    """

    key: str
    
    def __init__(self, key: str) -> None:
        self.key = key
        self.next = None
        
    def perform(self, node: jtt_tree.TreeNode) -> jtt_tree.TreeNode:
        """
        If the node is a dictionary, return the value at the key. 
        Otherwise, return nothing
        """
        if node.type == jtt_tree.NodeType.OBJECT:
            return node.value.get(self.key, None)
        else:
            return None
        
        
class QueryOperationChain:
    """
    This class is used to represent the operations in a query in proper order.
    An operation chain, when executed, should resolve to a ObjectTreeNode that contains the valid 
    results.
    """
    
    head: Optional[QueryOperation]
    
    def __init__(self, head: QueryOperation) -> None:
        self.head = head
        
    def append(self, op: QueryOperation) -> None:
        """
        Append an operation to the end of the chain, including any downstream attached operations.
        
        Args:
            op: The operation to append.
        """
        
        if not self.head:
            self.head = op
            return 
          
        current = self.head
        while current.next:
            current = current.next
        current.next = op 
        
    def has_next(self) -> bool:
        """
        Returns True if there are more operations to perform.
        """
        return self.head is not None    
    
    def pop_operation(self, tree: jtt_tree.TreeNode) -> Optional[jtt_tree.TreeNode]:
        """
        Removes the first operation from the chain and returns its result.
        """
        if self.head:
            op = self.head
            self.head = self.head.next
            return op.perform(tree)
        return None