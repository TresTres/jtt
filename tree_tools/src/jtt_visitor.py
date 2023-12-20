import typing
import math

from src import jtt_tree

class NodeVisitor:
    
    tree: jtt_tree.TreeNode
    
    def visit_string_node(self, node: jtt_tree.StringTreeNode) -> None:
        pass
    
    def visit_int_node(self, node: jtt_tree.IntTreeNode) -> None:
        pass
    
    def visit_array_node(self, node: jtt_tree.ListTreeNode) -> None:
        pass
    
    def visit_object_node(self, node: jtt_tree.ObjectTreeNode) -> None:
        pass
    

class NodeQuery(NodeVisitor):
    
    """
    This class is used to query a tree for a given path.
    """
    
    path: typing.List[str]
    results: typing.List[jtt_tree.TreeNode]
    wildcard: str = '**'
    
    def __init__(self, tree: jtt_tree.TreeNode, path: typing.List[str]):
        self.tree = tree
        self.path = path
        self.results = []
        
    def collect_results(self) -> typing.List[jtt_tree.TreeNode]:
        """
        Collect the results of the query.
        """
        self.tree.accept_visitor(self)
        return self.results
        
    def visit_string_node(self, node: jtt_tree.StringTreeNode) -> None:
        """
        Add the node to the results if the path is empty.
        """
        if not self.path:
            self.results.append(node)
                
    def visit_int_node(self, node: jtt_tree.IntTreeNode) -> None:
        """
        Add the node to the results if the path is empty.
        """
        if not self.path:
            self.results.append(node)

    def visit_array_node(self, node: jtt_tree.ListTreeNode) -> None:
        """
        If the path is empty, add the node to the results.
        If the current term in the path is a wildcard, recurse on all nodes.
        Otherwise, recurse on the node that matches the specified index.
        Recursion means the creation of a new NodeQuery object.
        """
        if not self.path:
            self.results.append(node)
            return
        term = self.path.pop(0)
        if term.isdigit():
            index = int(term)
            if index < len(node.value):
                visitor = NodeQuery(node.value[index], self.path.copy())
                self.results.extend(visitor.collect_results()) 
            return                
        if term == self.wildcard:
            for child in node.value:
                visitor = NodeQuery(child, self.path.copy())
                self.results.extend(visitor.collect_results())
        return

    def visit_object_node(self, node: jtt_tree.ObjectTreeNode) -> None:
        """
        If the path is empty, add the node to the results.
        If the current term in the path is a wildcard, recurse on all nodes.
        Otherwise, recurse on nodes that matches the specified key.
        Recursion means the creation of a new NodeQuery object.
        """
        if not self.path:
            self.results.append(node)
            return
        term = self.path.pop(0)
        if term == self.wildcard:
            for child in node.value.values():
                visitor = NodeQuery(child, self.path.copy())
                self.results.extend(visitor.collect_results())
            return
        if term in node.value:
            visitor = NodeQuery(node.value[term], self.path.copy())
            self.results.extend(visitor.collect_results())
        return 