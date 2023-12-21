import pytest

from tree_tools.src import jtt_tree


class TestTree:
    @pytest.mark.parametrize("data", [(None), (1), (1.0), ("a"), (True), (False), ([])])
    def test_tree_creation_failure(self, data):
        """Test tree creation failure"""

        with pytest.raises(ValueError):
            jtt_tree.create_tree(data)

    def test_tree_creation_success(self, fixture_sample_data_types):
        """Test tree creation success"""

        tree = jtt_tree.create_tree(fixture_sample_data_types)

        assert tree.value["a"].value == 1
        assert tree.value["b"].value == "2"
        assert tree.value["c"].value["d"].value == 3
        assert tree.value["c"].value["e"].value == "4"
        assert tree.value["f"].value[0].value == 5
        assert tree.value["f"].value[1].value == "6"
        assert tree.value["f"].value[2].value["g"].value == 7
        assert tree.value["h"].value is None
        assert tree.value["i"].value == 1.5
        assert tree.value["j"].value == {}

    def test_tree_children_counts(self, fixture_sample_data_types):
        """Test tree children counts"""

        tree = jtt_tree.create_tree(fixture_sample_data_types)

        assert tree.descendant_count == 13
        assert tree.value["a"].descendant_count == 0
        assert tree.value["b"].descendant_count == 0
        assert tree.value["c"].descendant_count == 2
        assert tree.value["c"].value["d"].descendant_count == 0
        assert tree.value["c"].value["e"].descendant_count == 0
        assert tree.value["f"].descendant_count == 4
        assert tree.value["f"].value[0].descendant_count == 0
        assert tree.value["f"].value[1].descendant_count == 0
        assert tree.value["f"].value[2].descendant_count == 1
        assert tree.value["f"].value[2].value["g"].descendant_count == 0
        assert tree.value["h"].descendant_count == 0
        assert tree.value["i"].descendant_count == 0
        assert tree.value["j"].descendant_count == 0
