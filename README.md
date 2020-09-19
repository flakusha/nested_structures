# nested_structures
Naive implementation of nested structures in Python

## Nested Dictionary
Data structure is built above the default dictionary implementation in Python,
so it can use all the methods default dict() provides.

This implementation is pretty similar to trie data structure, but it's possible
to hold more that one char in each key. Pretty fast lookups are among advantages
of this data structure. Worst case scenario is usually O(m), where m is the
length of string provided for lookup, but generally task complexity is around
O(1).

Docstrings are describing the inner mechanics of methods and included in source
code. For more complex and tested implementations please consider using
[glom](https://github.com/mahmoud/glom/).
