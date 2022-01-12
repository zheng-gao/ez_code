from fixture.list import s_list, c_list, r_list


def test_print():
    pass

def test_is_copied():
    assert s_list.is_copied(c_list)

def test_copy():
    assert s_list.is_copied(s_list.copy())
    assert not s_list.is_copied(r_list)

def test_reverse():
    reversed_list = s_list.copy()
    reversed_list.reverse()
    assert reversed_list.is_copied(r_list)
