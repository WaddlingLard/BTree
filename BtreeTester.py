import pytest

from Btree import Btree
from BtreeNode import BtreeNode
from search_methods import binary_search

# -------------------------------
## SETUP METHODS
# -------------------------------

# Split_btree_1 - Creates a btree that has a split occur so there is a root pointing to two children
# Returns (Btree)
def split_btree_1() -> Btree:
    btree: Btree = Btree(4)

    # Insertions will create a split
    btree.insert(1)
    btree.insert(2)
    btree.insert(3)
    btree.insert(4)
    btree.insert(5)

    return btree

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

def test_child_search_single_element_left_child():
    vals: list[int] = [3]

    assert child_search(vals, 0) == 0

def test_child_search_single_element_right_child():
    vals: list[int] = [3]

    assert child_search(vals, 5) == 1

def test_child_search_two_element_left_child():
    vals: list[int] = [3, 7]
    
    assert child_search(vals, 0) == 0

def test_child_search_two_element_middle_child():
    vals: list[int] = [3, 7]
    
    assert child_search(vals, 4) == 1

def test_child_search_two_element_last_child():
    vals: list[int] = [3, 7]
    
    assert child_search(vals, 8) == 2

def test_child_search_multi_element_leftmost_child():
    vals: list[int] = [1, 6, 11, 39, 100, 1356]

    assert child_search(vals, 0) == 0

def test_child_search_multi_element_inner_child():
    vals: list[int] = [1, 6, 11, 39, 100, 1356]

    assert child_search(vals, 54) == 4

def test_child_search_multi_element_rightmost_child():
    vals: list[int] = [1, 6, 11, 39, 100, 1356]

    assert child_search(vals, 2000) == 6

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

def test_exists_after_insert_root_btree():
    btree: Btree = Btree(4)
    
    btree.insert(1)

    assert btree.exists(1) == True
    del btree

def test_exists_empty_root_btree():
    btree: Btree = Btree(4)
    
    assert btree.exists(1) == False
    del btree

# def test_not_exists_after_insert_root_btree():
#     btree: Btree = Btree(4)
    
#     btree.insert(1)

#     assert btree.exists(2) == False
#     del btree

def test_insert_split_full_root_check_root_btree():
    btree: Btree = Btree(4)
    btree.root.node = [1,2,4,5]

    btree.insert(3)

    assert f'{btree.output_root()}' == '[3]'
    del btree

def test_insert_split_full_root_validate_children_btree():
    btree: Btree = Btree(4)
    btree.root.node = [1,2,4,5]

    btree.insert(3)

    result: list[BtreeNode] = btree.retrieve_children()
    num_of_children = len(result)

    contents: list[list[any]] = [x.get_node_contents() for x in result]

    assert num_of_children == 2
    assert contents == [[1,2],[4,5]]
    # assert f'{btree.output_root()}' == '[3]'
    del btree

def test_insert__left_child_split_btree_1():
    btree: Btree = split_btree_1()

    btree.insert(0)

    assert btree.retrieve_children()[0].search(0) == 0
    del btree

def test_insert_split_full_child_validate_children_btree():
    btree: Btree = split_btree_1()

    # Fill child node
    btree.insert(6)
    btree.insert(7)

    # New split occurs with this insertion
    btree.insert(8)

    result: list[BtreeNode] = btree.retrieve_children()
    num_of_children: int = len(result)

    contents: list[list[any]] = [x.get_node_contents() for x in result]

    assert num_of_children == 2
    assert contents == [[1,2],[4,5],[7,8]]
    assert btree._get_root().print_node() == [3,6]
    
    del btree

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

def test_insert_full_root_no_split_check_root_btree():
    btree: Btree = Btree(4)

    btree.insert(1)
    btree.insert(4)
    btree.insert(3)
    btree.insert(6)

    # Disabled splitting so 10 stays in the root
    btree.insert(10, True)
    
    assert btree.exists(10) == True
    del btree

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
    assert binary_search(node.node, 5) == 4
    del node

def test_insert_till_full_btreenode():
    node: BtreeNode = BtreeNode(4)
    
    node.insert(1)
    node.insert(2)
    node.insert(3)

    assert node.insert(4) == True
    assert node.insert(5) == False
    assert binary_search(node.node, 5) == 4
    del node

def test_insert_duplicate_key_btreenode():
    node: BtreeNode = BtreeNode(4)
    node.node = [1]

    with pytest.raises(Exception, match="Duplicate Key"):
        node.insert(1)