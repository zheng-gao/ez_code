from ezcode.Bit import bool_list_to_number


def test_bool_list_to_number():
    assert bool_list_to_number([]) == None
    assert bool_list_to_number([False]) == 0
    assert bool_list_to_number([True]) == 1
    assert bool_list_to_number([False, False]) == 0
    assert bool_list_to_number([False, True]) == 1
    assert bool_list_to_number([True, False]) == 2
    assert bool_list_to_number([True, True]) == 3
    assert bool_list_to_number([False, True, False]) == 2
    assert bool_list_to_number([True, False, False]) == 4
    assert bool_list_to_number([True, False, True]) == 5
    assert bool_list_to_number([True, True, True]) == 7
    assert bool_list_to_number([True, False, True, False]) == 10
    assert bool_list_to_number([], reverse=True) == None
    assert bool_list_to_number([False], reverse=True) == 0
    assert bool_list_to_number([True], reverse=True) == 1
    assert bool_list_to_number([False, False], reverse=True) == 0
    assert bool_list_to_number([False, True], reverse=True) == 2
    assert bool_list_to_number([True, False], reverse=True) == 1
    assert bool_list_to_number([True, True], reverse=True) == 3
    assert bool_list_to_number([False, True, False], reverse=True) == 2
    assert bool_list_to_number([True, False, False], reverse=True) == 1
    assert bool_list_to_number([True, False, True], reverse=True) == 5
    assert bool_list_to_number([True, True, True], reverse=True) == 7
    assert bool_list_to_number([True, False, True, False], reverse=True) == 5