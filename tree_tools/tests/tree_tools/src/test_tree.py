import pytest

from tree_tools.src.jtt_tree import create_tree

class TestTree:
    
    @pytest.mark.parametrize(
        "data", 
        [
            (None),
            (1),
            (1.0),
            ('a'),
            (True),
            (False),
            ([])
        ]
    )
    def test_tree_creation_failure(self, data):
        """Test tree creation failure"""
        
        with pytest.raises(ValueError):
            create_tree(data)
            
            
    def test_tree_creation_success(self, fixture_sample_data):
        """Test tree creation success"""
        
        tree = create_tree(fixture_sample_data)
        
        assert tree.value['a'].value == 1
        assert tree.value['b'].value == '2'
        assert tree.value['c'].value['d'].value == 3
        assert tree.value['c'].value['e'].value == '4'
        assert tree.value['f'].value[0].value == 5
        assert tree.value['f'].value[1].value == '6'
        assert tree.value['f'].value[2].value['g'].value == 7
        
