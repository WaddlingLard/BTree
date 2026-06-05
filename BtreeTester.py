from Btree import Btree
from BtreeNode import BtreeNode
from binary_search import binary_search

# -------------------------------
## UTILITY TESTS
# -------------------------------
def test_search_single_element_success():
    vals: list[int] = [1]

    assert binary_search(vals, 1) == 0

# def test_search_single_element_failure():
#     vals: list[int] = [1]

#     assert binary_search(vals, 2) == -1

def test_search_single_element_failure():
    vals: list[int] = [2]

    assert binary_search(vals, 1) == -1

def test_search_double_element_success():
    vals: list[int] = [1,2]

    assert binary_search(vals, 2) == 1

def test_search_double_element_failure():
    vals: list[int] = [1,2]

    assert binary_search(vals, 3) == -1

def test_search_multi_element_success():
    vals: list[int] = [1,2,3]
    
    assert binary_search(vals, 3) == 2

def test_search_multi_element_failure():
    vals: list[int] = [1,2,3]
    
    assert binary_search(vals, 4) == -1

def test_search_many_element_success():
    vals: list[int] = [1,2,3,4,5,6,7,8,9,10]
    
    assert binary_search(vals, 10) == 9

def test_search_many_element_failure():
    vals: list[int] = [1,2,3,4,5,7,8,9,10,11]
    
    assert binary_search(vals, 6) == -1

# -------------------------------
## BTREE TESTS
# -------------------------------
def test_create_btree_even_keys():
    btree: Btree = Btree(4)
    
    assert btree.max_keys == 4 and btree.min_keys == 2
    del btree

def test_create_btree_odd_keys():
    btree: Btree = Btree(3)

    assert btree.max_keys == 3 and btree.min_keys == 1
    del btree

# def test_insert_empty_root_btree():
#     btree: Btree = Btree(4)

#     assert btree.insert(1) == False
#     del btree

# def test_insert_partial_root_btree():
#     btree: Btree = Btree(4)
#     btree.root.node = [1,2]

#     assert btree.insert(3) == False
#     del btree

# def test_insert_full_root_btree():
#     btree: Btree = Btree(4)
#     btree.root.node = [1,2,3,4]

#     assert btree.insert(5) == True
#     del btree

# -------------------------------
## BTREENODE TESTS
# -------------------------------
def test_create_btreenode():
    node: BtreeNode = BtreeNode(4)

    assert node.number_of_children == 0 and node.is_leaf == True and node.node_size == 4
    del node

def test_insert_empty_btreenode():
    node: BtreeNode = BtreeNode(4)

    assert node.insert(1) == True
    del node

def test_insert_partial_btreenode():
    node: BtreeNode = BtreeNode(4)
    node.node = [1,2]

    assert node.insert(3) == True
    del node

def test_insert_full_btreenode():
    node: BtreeNode = BtreeNode(4)
    node.node = [1,2,3,4]

    # Node violates the invariant
    assert node.insert(5) == False
    del node
