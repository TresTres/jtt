import pytest

from tree_tools.src import jtt_tree


class TestTree:
    @pytest.mark.parametrize("data", [(None), (1), (1.0), ("a"), (True), (False), ([])])
    def test_tree_creation_failure(self, data):
        """Test tree creation failure"""

        with pytest.raises(ValueError):
            jtt_tree.create_tree(data)

    def test_tree_creation_success(self, fixture_sample_data_types):
        """Test tree creation success -- don't auto parse strings into numbers"""

        tree = jtt_tree.create_tree(fixture_sample_data_types)

        assert tree.type == jtt_tree.NodeType.OBJECT
        assert tree.value["a"].type == jtt_tree.NodeType.NUMBER
        assert tree.value["b"].type == jtt_tree.NodeType.STRING
        assert tree.value["c"].type == jtt_tree.NodeType.NUMBER
        assert tree.value["d"].type == jtt_tree.NodeType.BOOLEAN
        assert tree.value["e"].type == jtt_tree.NodeType.OBJECT
        assert tree.value["e"].value["f"].type == jtt_tree.NodeType.NUMBER
        assert tree.value["e"].value["g"].type == jtt_tree.NodeType.STRING
        assert tree.value["e"].value["h"].type == jtt_tree.NodeType.BOOLEAN
        assert tree.value["i"].type == jtt_tree.NodeType.ARRAY
        assert tree.value["i"].value[0].type == jtt_tree.NodeType.NUMBER
        assert tree.value["i"].value[1].type == jtt_tree.NodeType.STRING
        assert tree.value["i"].value[2].type == jtt_tree.NodeType.BOOLEAN
        assert tree.value["i"].value[3].type == jtt_tree.NodeType.OBJECT
        assert tree.value["i"].value[3].value["j"].type == jtt_tree.NodeType.NUMBER
        assert tree.value["k"].type == jtt_tree.NodeType.NULL
        assert tree.value["l"].type == jtt_tree.NodeType.OBJECT

    def test_tree_children_counts(self, fixture_sample_data_types):
        """Test tree children counts"""

        tree = jtt_tree.create_tree(fixture_sample_data_types)

        assert tree.descendant_count == 16
        assert tree.value["e"].descendant_count == 3
        assert tree.value["i"].descendant_count == 5
        assert tree.value["i"].value[3].descendant_count == 1
