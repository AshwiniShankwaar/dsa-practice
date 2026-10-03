# 11 — Tries

## Idea
A trie stores words letter by letter. Words with the same start share the same path.
Looking up a word costs O(length of word), no matter how many words you stored.

```
        root
       /    \
      c      d
      |      |
      a      o
      |      |
      t*     g*     (* = a full word ends here: "cat", "dog")
```

## Template
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_end = True

    def _walk(self, s):
        node = self.root
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def search(self, word):          # is this a full word?
        node = self._walk(word)
        return bool(node and node.is_end)

    def starts_with(self, prefix):   # does any word start like this?
        return self._walk(prefix) is not None
```

## Where it helps
- Autocomplete and prefix checks.
- Word Search II: walk the grid and the trie together; stop early when the path is not in the trie.
- Maximum XOR: store numbers as bits and greedily pick the opposite bit.

## Classic problems
Implement Trie, Add and Search Word (with `.` wildcard), Word Search II, Longest Common Prefix, Replace Words.

## Mistakes
- Mixing up `search` (full word) and `starts_with` (prefix). `is_end` is the difference.
