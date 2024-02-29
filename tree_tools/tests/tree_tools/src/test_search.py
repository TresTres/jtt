import pytest
from typing import Dict, Any

from tree_tools.src.search import jmespath_search

class TestSearchSampleData:
    
    
    @pytest.mark.parametrize(
        "query,expected_result",
        [
            ("a", 1),
            ("b", "2"),
            ("c", 1.5),
            ("d", True),
            ("e", {"f": 3, "g": "4", "h": False}),
            ("e.f", 3),
            ("e.g", "4"),
            ("e.h", False),
        ],
    )
    def test_search_simple_identifier_query(self, fixture_sample_data_types: Dict[str, Any], query: str, expected_result: Any):
        
        results = jmespath_search(query, fixture_sample_data_types)
        assert results == expected_result