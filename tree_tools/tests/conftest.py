import pytest


@pytest.fixture()
def fixture_sample_data():
    data = {
        "a": 1,
        "b": "2",
        "c": {
            "d": 3,
            "e": "4",
        },
        "f": [5, "6", {"g": 7}],
    }
    return data.copy()
