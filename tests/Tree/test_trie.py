from ezcode.Tree.trie import Trie, SuffixTrie


def test_trie():
    trie = Trie()
    for word in ["code", "coke", "coffee", "cod"]:
        trie.add(word)
    trie_string = """
^:4 -> c:4 -> o:4 -> d:2:$ -> e:1:$
^:4 -> c:4 -> o:4 -> k:1 -> e:1:$
^:4 -> c:4 -> o:4 -> f:1 -> f:1 -> e:1 -> e:1:$
"""[1:]
    assert str(trie) == trie_string
    assert trie.size() == 4
    assert trie.longest_common_prefix() == list("co")
    assert trie.contains("cof")
    assert not trie.contains("cofe")
    assert trie.contains("coffee", strict=True)
    assert not trie.contains("cof", strict=True)
    assert trie.prefix_wildcard(list("co")) == [list("cod"), list("code"), list("coke"), list("coffee")]


def test_suffix_trie():
    suffix_trie = SuffixTrie("abcd")
    suffix_trie_string = """
^:4 -> a:1 -> b:1 -> c:1 -> d:1:$
^:4 -> b:1 -> c:1 -> d:1:$
^:4 -> c:1 -> d:1:$
^:4 -> d:1:$
"""[1:]
    assert str(suffix_trie) == suffix_trie_string
