from Btree import Btree
from BtreeNode import BtreeNode

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
