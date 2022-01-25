from fixture.list import s_list, s_list_copied, s_list_reversed


def test_print():
    pass

def test_is_copied():
    assert s_list.is_copied(s_list_copied)

def test_copy():
    assert s_list.copy().is_copied(s_list_copied)
    assert not s_list.is_copied(s_list_reversed)

def test_reverse():
    reversed_list = s_list.copy()
    reversed_list.reverse()
    assert reversed_list.is_copied(s_list_reversed)
