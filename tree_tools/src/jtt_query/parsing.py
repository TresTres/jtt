from typing import List
import re


from tree_tools.src.jtt_query.operations import QueryOperationChain, KeySelectOperation


PATTERN_START_WITH_WORD = re.compile(r"[a-zA-Z_]+")
PATTERN_QUOTE_CHARACTERS = re.compile(r'["\']')


class JMESPathValidationError(Exception):
    pass


class JMESPathParser:
    """
    This class is used to parse JMESPath query strings into query operations to execute.
    JMESPath is a query language for JSON-like data, explained in detail at https://jmespath.org/.
    """

    identifiers: List[str]
    operation_queue: QueryOperationChain

    def __init__(self) -> None:
        self.identifiers = []
        self.operation_queue = QueryOperationChain()

    def validate_query(self, query: str) -> None:
        """
        This method is used to validate a query string to ensure it is a valid JMESPath query.
        Raises JMESPathValidationError if the query is invalid.

        Args:
            query: The query string to validate.
        """
        if not query:
            raise JMESPathValidationError("Query string cannot be empty.")

        if not PATTERN_START_WITH_WORD.match(
            query
        ) and not PATTERN_QUOTE_CHARACTERS.match(query):
            raise JMESPathValidationError(
                "Query string must start with a word character or a quote character."
            )

    def tokenize(self, query: str) -> None:
        """
        This method breaks up a query string into tokens using expected delimiters and special symbols.
        A query string is processed from left to right.

        Args:
            query: The query string to tokenize.
        """

        if "." in query:
            self.identifiers = query.split(".")
        else:
            self.identifiers.append(query)

    def create_query_operations(self) -> None:
        """
        This method creates query objects from stored tokens and adds them to the operation queue.
        """
        for identifier in self.identifiers:
            key_operation = KeySelectOperation(identifier)
            self.operation_queue.append(key_operation)

    def parse(self, query: str) -> QueryOperationChain:
        """
        Main method to parse a query string into a query chain.
        This calls validate_query, and may raise a JMESPathValidationError.

        Args:
            query: The query string to parse.
        """

        self.validate_query(query)
        self.tokenize(query)
        self.create_query_operations()
        return self.operation_queue
