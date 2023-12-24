import itertools

from tree_tools.src import jtt_visitor


class TestNodeQuery:
    def test_blank_query(
        self, fixture_sample_data_type_tree, fixture_sample_data_types
    ):
        """Test blank query will deliver the root node"""

        query = jtt_visitor.NodeQueryEvaluator(fixture_sample_data_type_tree, [])
        results = query.collect_results()

        assert len(results) == 1
        assert results[0].value.keys() == fixture_sample_data_types.keys()

    def test_single_wildcard_query(
        self, fixture_sample_data_type_tree, fixture_sample_data_types
    ):
        """Test single wildcard will deliver all nodes underneath the root node"""

        wildcard_query = jtt_visitor.NodeQueryEvaluator(fixture_sample_data_type_tree, ["**"])
        results = wildcard_query.collect_results()

        assert len(results) == len(fixture_sample_data_types)

    def test_not_found_query(self, fixture_sample_data_type_tree):
        """Test that a query that doesn't match anything returns an empty list"""

        query = jtt_visitor.NodeQueryEvaluator(fixture_sample_data_type_tree, ["z"])
        results = query.collect_results()

        assert not results

    def test_object_key_query(self, fixture_pokemon_tree):
        """Test that data is extracted from objects using keys"""

        query = jtt_visitor.NodeQueryEvaluator(fixture_pokemon_tree, ["pokemon", "**", "id"])
        results = query.collect_results()
        assert len(results) == 151
        assert [r.value for r in results] == list(range(1, 152))

    def test_list_index_query(self, fixture_pokemon_tree):
        """Test that data is extracted from lists using indices"""

        query = jtt_visitor.NodeQueryEvaluator(
            fixture_pokemon_tree, ["pokemon", "**", "multipliers", "1"]
        )
        results = query.collect_results()
        assert len(results) == 37
        compare_results = []
        for p in fixture_pokemon_tree.value["pokemon"].value:
            if p.value["multipliers"].value and len(p.value["multipliers"].value) > 1:
                compare_results.append(p.value["multipliers"].value[1].value)
        assert [r.value for r in results] == compare_results
