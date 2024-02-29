from typing import Dict, Any, Optional

from tree_tools.src.jtt_tree import create_tree, NullTreeNode
from tree_tools.src.jtt_query import queries
from tree_tools.src.jtt_query import parsing


def jmespath_search(query: str, tree: Dict[str, Any]) -> Dict[str, Any]:
    """
    This function is used to search for nodes in a TreeNode object using a JMESPath query string.
    
    Args:
        query: The JMESPath query string to use.
        tree: The TreeNode to search.
        
    Returns:
        A list of TreeNode objects that match the query.
    """
    tree = create_tree(tree)
    parser = parsing.JMESPathParser()
    operation_chain = parser.parse(query)
    processor = queries.QueryProcessor(tree, operation_chain)
    results = processor.execute()
    return results.serialize()
    