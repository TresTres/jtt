import typing

def index_within_list(index: int, l: typing.List[typing.Any]) -> bool:
    """
    Return True if the index is within the bounds of the list, False otherwise.
    """
    return len(l) > index >= -len(l)