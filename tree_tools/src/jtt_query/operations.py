from abc import abstractmethod
from typing import Optional, Generator

from tree_tools.src import jtt_tree

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

    
class KeySelectOperation(QueryOperation):
    """
    This class is used to represent the key selection in a query.  
    A key selection only applies to ObjectTreeNodes and returns the TreeNode stored at the specified key.
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
    
    def __init__(self) -> None:
        self.head = None

    def __len__(self) -> int:
        """
        Returns the number of operations in the chain.
        """
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count
        
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
    
    def pop_operation(self) -> Optional[QueryOperation]:
        """
        Removes the first operation from the chain and returns it.
        
        Args:
            tree: The TreeNode to perform the operation on.
        """
        if self.head:
            op = self.head
            self.head = self.head.next
            return op
        return None
    
    def operations(self) -> Generator[QueryOperation, None, None]:
        """
        Returns a generator that yields each operation in the chain.
        This is a destructive operation as each yield calls pop_operation.
        """
        
        while self.has_next():
            yield self.pop_operation()