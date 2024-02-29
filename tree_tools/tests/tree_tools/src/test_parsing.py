import pytest 

from tree_tools.src.jtt_query import parsing

@pytest.fixture(scope='class')
def parser() -> parsing.JMESPathParser:
    return parsing.JMESPathParser()


class TestJMESPathParserValidation:

    def test_invalid_query_empty(self, parser: parsing.JMESPathParser):
        with pytest.raises(parsing.JMESPathValidationError) as validation_error:
            parser.validate_query('')
        assert "cannot be empty" in str(validation_error.value)
            
    @pytest.mark.parametrize(
        "query",
        [
            "1",
            "!",
            "@",
            "#",
            "$",
            "%",
            "^",
            "&",
            "*",
            "(",
            ")",
            "-",
            "+",
            "=",
            "{",
            "}",
            "[",
            "]",
            "|",
            "\\",
            ";",
            ":",
            "<",
            ">",
            ",",
            ".",
            "/",
            "?",
        ],
    )
    def test_invalid_query_start_with_special_character(self, parser: parsing.JMESPathParser, query: str):
        with pytest.raises(parsing.JMESPathValidationError) as validation_error:
            parser.validate_query(query)
        assert "must start with a word character or a quote character" in str(validation_error.value)

class TestJMESPathParserTokenization:
    
    
    def test_single_identifier_tokenization(self, parser: parsing.JMESPathParser):
        parser.tokenize('foo')
        assert parser.identifiers == ['foo']
    
    def test_identifier_tokenization(self, parser: parsing.JMESPathParser):
        parser.tokenize('foo.bar.baz')
        assert parser.identifiers == ['foo', 'bar', 'baz']
        
        
class TestJMESPathParserOperationCreation:
    
    def test_create_query_operations(self, parser: parsing.JMESPathParser):
        parser.identifiers = ['foo', 'bar', 'baz']
        parser.create_query_operations()
        assert len(parser.operation_queue) == 3
        ops = [op for op in parser.operation_queue]
        assert all(isinstance(op, parsing.KeySelectOperation) for op in ops)
        assert [op.key for op in ops] == ['foo', 'bar', 'baz']