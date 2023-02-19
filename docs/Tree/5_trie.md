# Trie
```python
>>> from ezcode.tree.trie import Trie
>>> trie = Trie()
>>> for word in ["today", "tomorrow", "tonight", "tobaco", "tod", "tony"]:
...     trie.add(list(word))
... 
>>> trie.size()
6
>>> trie.print()
^:6 -> t:6 -> o:6 -> d:2:$ -> a:1 -> y:1:$
^:6 -> t:6 -> o:6 -> m:1 -> o:1 -> r:1 -> r:1 -> o:1 -> w:1:$
^:6 -> t:6 -> o:6 -> n:2 -> i:1 -> g:1 -> h:1 -> t:1:$
^:6 -> t:6 -> o:6 -> n:2 -> y:1:$
^:6 -> t:6 -> o:6 -> b:1 -> a:1 -> c:1 -> o:1:$
>>> trie.contains(list("toni"))
True
>>> trie.contains(list("tonx"))
False
>>> trie.contains(list("toni"), strict=True)
False
>>> trie.contains(list("tod"), strict=True)
True
>>> "".join(trie.longest_common_prefix())
'to'
>>> for word in trie.prefix_wildcard(list("ton")):
...     print("".join(word))
... 
tonight
tony
```
# Suffix Trie
```python
>>> from ezcode.tree.trie import SuffixTrie
>>> suffix_trie = SuffixTrie("abcab")
>>> suffix_trie.print()
^:5 -> a:2 -> b:2:$ -> c:1 -> a:1 -> b:1:$
^:5 -> b:2:$ -> c:1 -> a:1 -> b:1:$
^:5 -> c:1 -> a:1 -> b:1:$
```