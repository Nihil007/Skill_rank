# import result from freq_element
from freq_elements import mostfrequent

def test_case1():
    assert mostfrequent([1, 1, 1, 2, 2, 3], 1) == [1]

def test_case2():
    assert mostfrequent([5, 5, 5, 5], 1) == [5]

def test_case3():
    # used set to accept any order
    assert set(mostfrequent([1, 2, 3, 4, 5], 3)) == {1, 2, 3}

def test_case4():
    assert mostfrequent([42], 1) == [42]

def test_case5():
    # used set to accept any order
    assert set(mostfrequent([1, 2, 3], 5)) == {1, 2, 3}

def test_case6():
    assert mostfrequent([3, 0, 1, 0], 1) == [0]

def test_case7():
    assert mostfrequent([7, 10, 11, 5, 2, 5, 5, 7, 11, 8, 9], 1) == [5]
