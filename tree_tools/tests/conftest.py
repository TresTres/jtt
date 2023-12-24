import pytest

import json

from tree_tools.src.jtt_tree import create_tree


@pytest.fixture()
def fixture_sample_data_types():
    data = {
        "a": 1,
        "b": "2",
        "c": 1.5,
        "d": True, 
        "e": {
            "f": 3,
            "g": "4",
            "h": False,
        },
        "i": [5, "6", True, {"j": 7}],
        "k": None,
        "l": {},
    }
    return data.copy()


@pytest.fixture()
def fixture_sample_data_type_tree(fixture_sample_data_types):
    return create_tree(fixture_sample_data_types)


@pytest.fixture()
def fixture_pokemon_tree():
    file = open("tree_tools/tests/test_jsons/pokemon.json")
    data = json.load(file)
    return create_tree(data)
