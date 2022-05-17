import pytest 

from split_events import find_precipitation_events


def test_standard_case():
    """single list"""
    test_list = [0,0,0,1,2,3,0,0,0]
    expected = [[1,2,3]]
    assert expected == find_precipitation_events(test_list, trigger_level=3)
    
def test_singlelist_begin():
    """single list at begin"""
    test_list = [1,2,3,0,0,0]
    expected = []
    assert expected == find_precipitation_events(test_list, trigger_level=3)
    
def test_singlelist_end():
    """single list at end"""
    test_list = [0,0,0,1,2,3]
    expected = []
    assert expected == find_precipitation_events(test_list, trigger_level=3)

def test_twolists_begin():
    """second list at begin"""
    test_list = [1,0,0,0,1,2,3,0,0,0]
    expected = [[1,2,3]]
    assert expected == find_precipitation_events(test_list, trigger_level=3)
    
def test_twolists_end():
    """second list at end"""
    test_list = [0,0,0,1,2,3,0,0,0,1]
    expected = [[1,2,3]]
    assert expected == find_precipitation_events(test_list, trigger_level=3)

def test_emptylist():
    test_list = []
    expected = []
    assert expected == find_precipitation_events(test_list, trigger_level=3)

def test_oneelement():
    test_list = [1]
    expected = []
    assert expected == find_precipitation_events(test_list, trigger_level=3)
    
def test_twolists_smallgap():
    test_list = [0,0,0,1,2,3,0,1,0,0,0]
    expected = []
    assert expected == find_precipitation_events(test_list, trigger_level=3)
    
def test_twolists_largegap():
    test_list = [0,0,0,1,2,3,0,0,0,0,1,0,0,0]
    expected = [[1,2,3],[1]]
    assert expected == find_precipitation_events(test_list, trigger_level=3)

def test_wrong_type():
    """If string data is given, an empty list will be the output"""
    test_list = ["0","0","0","1","0","0","0"]
    with pytest.raises(TypeError):
        find_precipitation_events(test_list, trigger_level=3)
        
def test_trigger_1():
    test_list = [0,1,0]
    with pytest.raises(ValueError):
        find_precipitation_events(test_list, trigger_level=1)
    
def test_trigger_2():
    test_list = [0,0,1,0,0]
    expected = [[1]]
    assert expected == find_precipitation_events(test_list, trigger_level=2)