import imp
import pytest 
import sys, os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from rolling_window import rolling_window_multiple_events


def test_largelist_smalllist():
    test_list = [[0.08, 0.13, 0.2, 0.28, 0.33, 0.31, 0.27, 0.09, 0.03], [0.01,0.02]]
    expected = {1: [0.33, 0.02], 2: [0.64, 0.03], 3: [0.92], 6: [1.52], 12: [], 18: [], 36: []}
    assert expected == rolling_window_multiple_events(test_list)

def test_largelist_smalllist2():
    test_list = [[0.08, 0.13, 0.2, 0.28, 0.33, 0.31, 0.27, 0.09, 0.03], [0.01]]
    expected = {1: [0.33, 0.01], 2: [0.64], 3: [0.92], 6: [1.52], 12: [], 18: [], 36: []}
    assert expected == rolling_window_multiple_events(test_list)

def test_smalllist_largelist():
    test_list = [[0.08, 0.01], [0.01,0.02]]
    expected = {1: [0.08, 0.02], 2: [0.09, 0.03], 3: [], 6: [], 12: [], 18: [], 36: []}
    assert expected == rolling_window_multiple_events(test_list)
    
def test_smalllist_largelist2():
    test_list = [[0.08], [0.01,0.02]]
    expected = {1: [0.08, 0.02], 2: [0.03], 3: [], 6: [], 12: [], 18: [], 36: []}
    assert expected == rolling_window_multiple_events(test_list)

def test_one_empty_list():
    test_list = [[]]
    expected = {1: [], 2: [], 3: [], 6: [], 12: [], 18: [], 36: []}
    assert expected == rolling_window_multiple_events(test_list)

def test_two_empty_lists():
    test_list = [[],[]]
    expected = {1: [], 2: [], 3: [], 6: [], 12: [], 18: [], 36: []}
    assert expected == rolling_window_multiple_events(test_list)