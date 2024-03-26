# Zip Trees

This is the implementation of the Zip Trees data structure as described in the paper "Zip Trees" by Robert E. Tarjan, Caleb C. Levy, Stephen Timmel in 2018.

## Skiplists

Zip Trees are a generalization of skiplists. Skiplists are a data structure that allows for fast search, insertion, and deletion of elements. They are similar to linked lists, but with additional pointers that allow for faster search times.

There's also an implementation of skiplists in this repository at [skiplists.py](skiplists.py). It also includes a helper function to convert a skiplist to a Zip Tree.

## Usage

```python
from zip_trees import ZipTree

# Create a new ZipTree
zip_tree = ZipTree()

# Insert a new element
zip_tree.insert(4, 'a', 2)
zip_tree.insert(5, 'b', 3)

# Find the element with key 4
zip_tree.find(4) # a
```
