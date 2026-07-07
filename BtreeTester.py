import pytest

from Btree import Btree
from BtreeNode import BtreeNode
from search_methods import binary_search, child_search

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

def split_btree_2() -> Btree:
    btree: Btree = Btree(4)

    btree.insert(-2)
    btree.insert(-1)
    btree.insert(1)
    btree.insert(3)
    btree.insert(4)
    btree.insert(5)
    btree.insert(7)
    btree.insert(8)
    btree.insert(11)
    btree.insert(12)
    btree.insert(13)
    btree.insert(18)
    btree.insert(19)
    btree.insert(20)
    
    # These are filling a child prep for a split on that node
    btree.insert(14)
    btree.insert(15)

    return btree

def split_btree_3() -> Btree:
    btree: Btree = Btree(4)

    btree.insert(0)
    btree.insert(1)
    btree.insert(2)
    btree.insert(3)
    btree.insert(4)
    btree.insert(5)
    btree.insert(6)
    btree.insert(7)
    btree.insert(8)
    btree.insert(9)
    btree.insert(10)

    return btree

# -------------------------------
## UTILITY TESTS
# -------------------------------
def test_search_single_element_success():
    vals: list[int] = [1]

    assert binary_search(vals, 1)[1] == 0

# def test_search_single_element_failure():
#     vals: list[int] = [1]

#     assert binary_search(vals, 2)[1] == -1

def test_search_single_element_failure():
    vals: list[int] = [2]

    assert binary_search(vals, 1)[1] == -1

def test_search_double_element_success():
    vals: list[int] = [1,2]

    assert binary_search(vals, 2)[1] == 1

def test_search_double_element_failure():
    vals: list[int] = [1,2]

    assert binary_search(vals, 3)[1] == -1

def test_search_multi_element_success():
    vals: list[int] = [1,2,3]
    
    assert binary_search(vals, 3)[1] == 2

def test_search_multi_element_failure():
    vals: list[int] = [1,2,3]
    
    assert binary_search(vals, 4)[1] == -1

def test_search_many_element_success():
    vals: list[int] = [1,2,3,4,5,6,7,8,9,10]
    
    assert binary_search(vals, 10)[1] == 9

def test_search_many_element_failure():
    vals: list[int] = [1,2,3,4,5,7,8,9,10,11]
    
    assert binary_search(vals, 6)[1] == -1

def test_child_search_single_element_left_child():
    vals: list[int] = [3]

    assert child_search(vals, 0)[1] == 0

def test_child_search_single_element_right_child():
    vals: list[int] = [3]

    assert child_search(vals, 5)[1] == 1

def test_child_search_two_element_left_child():
    vals: list[int] = [3, 7]
    
    assert child_search(vals, 0)[1] == 0

def test_child_search_two_element_middle_child():
    vals: list[int] = [3, 7]
    
    assert child_search(vals, 4)[1] == 1

def test_child_search_two_element_last_child():
    vals: list[int] = [3, 7]
    
    assert child_search(vals, 8)[1] == 2

def test_child_search_multi_element_leftmost_child():
    vals: list[int] = [1, 6, 11, 39, 100, 1356]

    assert child_search(vals, 0)[1] == 0

def test_child_search_multi_element_inner_child():
    vals: list[int] = [1, 6, 11, 39, 100, 1356]

    assert child_search(vals, 54)[1] == 4

def test_child_search_multi_element_rightmost_child():
    vals: list[int] = [1, 6, 11, 39, 100, 1356]

    assert child_search(vals, 2000)[1] == 6

# -------------------------------
## BTREE TESTS
# -------------------------------
def test_exists_root_btree():
    btree: Btree = split_btree_1()

    assert btree.exists(3) == btree._get_root()
    assert btree.validate_invariants() == None
    del btree

def test_exists_left_node_btree():
    btree: Btree = split_btree_1()

    assert btree.exists(5).get_node_contents() == [4,5]
    assert btree.validate_invariants() == None
    del btree

def test_exists_right_node_btree():
    btree: Btree = split_btree_1()

    assert btree.exists(1).get_node_contents() == [1,2]
    assert btree.validate_invariants() == None
    del btree

def test_exists_expected_fail_btree(): 
    btree: Btree = split_btree_1()

    assert btree.exists(10) == None
    assert btree.validate_invariants() == None
    del btree

def test_create_btree_even_keys():
    btree: Btree = Btree(4)
    
    assert btree.max_keys == 4 and btree.min_keys == 2
    assert btree.validate_invariants() == None
    del btree

def test_create_btree_odd_keys():
    btree: Btree = Btree(3)

    assert btree.max_keys == 3 and btree.min_keys == 1
    assert btree.validate_invariants() == None
    del btree

def test_exists_after_insert_root_btree():
    btree: Btree = Btree(4)
    
    btree.insert(1)

    assert btree.exists(1) == btree._get_root()
    assert btree.validate_invariants() == None
    del btree

def test_exists_empty_root_btree():
    btree: Btree = Btree(4)
    
    assert btree.exists(1) == None
    assert btree.validate_invariants() == None
    del btree

def test_not_exists_after_insert_root_btree():
    btree: Btree = Btree(4)
    
    btree.insert(1)

    assert btree.exists(2) == None
    assert btree.validate_invariants() == None
    del btree

def test_insert_preexisting_btree(capsys):
    btree: Btree = Btree(4)
    
    btree.insert(1)
    btree.insert(1)

    streams = capsys.readouterr()
    assert streams.out == 'Key is already present in the Btree!\n'

    assert btree.exists(2) == None
    assert btree.validate_invariants() == None
    del btree

def test_insert_split_full_root_check_root_btree():
    btree: Btree = Btree(4)
    btree.root.node = [1,2,4,5]

    btree.insert(3)

    assert f'{btree.root.get_node_contents()}' == '[3]'
    assert btree.validate_invariants() == None
    del btree

def test_insert_split_full_root_validate_children_btree():
    btree: Btree = Btree(4)
    btree.root.node = [1,2,4,5]

    btree.insert(3)

    result: list[BtreeNode] = btree._retrieve_children()
    num_of_children = len(result)

    contents: list[list[any]] = [x.get_node_contents() for x in result]

    assert num_of_children == 2
    assert contents == [[1,2],[4,5]]
    assert btree._get_root().get_node_contents() == [3]
    assert btree.validate_invariants() == None
    del btree

# def test_insert_left_child_split_btree_1():
#     btree: Btree = split_btree_1()

#     btree.insert(0)

#     assert btree.retrieve_children()[0].search(0)[1] == 0
#     del btree

def test_insert_split_full_right_child_validate_children_btree():
    btree: Btree = split_btree_1()

    # Fill child node
    btree.insert(6)
    btree.insert(7)

    # New split occurs with this insertion
    btree.insert(8)

    # Get children of the root
    result: list[BtreeNode] = btree._retrieve_children()
    num_of_children: int = len(result)

    contents: list[list[any]] = [x.get_node_contents() for x in result]

    assert num_of_children == 3
    assert contents == [[1,2],[4,5],[7,8]]
    assert btree._get_root().print_node() == str([3,6])    
    assert btree.validate_invariants() == None

    del btree

def test_insert_split_full_left_child_validate_children_btree():
    btree: Btree = split_btree_1()

    btree.insert(0)
    btree.insert(-1)

    # Split occurs with this insertion
    btree.insert(-2)

    result: list[BtreeNode] = btree._retrieve_children()
    num_of_children: int = len(result)

    contents: list[list[any]] = [x.get_node_contents() for x in result]

    assert num_of_children == 3
    assert contents == [[-2,-1],[1,2],[4,5]]
    assert btree._get_root().print_node() == str([0,3])
    assert btree.validate_invariants() == None

    del btree

# def test_insert_recursive_split_on_full_root_validate_btree():
    # btree: Btree = split_btree_2

    # Split that will lead to a root split
    # btree.insert(16)

    # assert num_of_children = 


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
    
    assert btree.exists(10) == btree._get_root()
    assert btree.validate_invariants() != None

    del btree

def test_delete_single_element_root_btree():
    btree: Btree = Btree(4)

    btree.insert(1)

    assert btree._get_root().get_node_contents() == [1]
    
    element: object | None = btree.delete(1)

    assert element == 1
    assert btree._get_root().get_node_contents() == []
    assert btree.validate_invariants() == None
    del btree

def test_delete_multi_element_root_btree():
    btree: Btree = Btree(4)

    btree.insert(1)
    btree.insert(2)
    btree.insert(3)

    assert btree._get_root().get_node_contents() == [1,2,3]
    
    element: object | None = btree.delete(1)

    assert element != None and element == 1
    assert btree._get_root().get_node_contents() == [2,3]
    assert btree.validate_invariants() == None
    del btree    

def test_delete_fail_multi_element_root_btree(capsys):
    btree: Btree = Btree(4)

    btree.insert(1)
    btree.insert(2)
    btree.insert(3)

    assert btree._get_root().get_node_contents() == [1,2,3]
    
    element: object | None = btree.delete(0)

    streams = capsys.readouterr()

    assert streams.out == "Key doesn't exist in the Btree!\n"
    assert element == None
    assert btree._get_root().get_node_contents() == [1,2,3]
    assert btree.validate_invariants() == None
    del btree    

def test_delete_single_element_left_child_btree():
    btree: Btree = split_btree_1()

    element: object | None = btree.delete(1)

    assert element == 1
    assert btree._get_root().get_node_contents() == [2,3,4,5]
    assert btree._get_root().get_leaf_status() == True
    assert btree.validate_invariants() == None
    del btree    

def test_delete_single_element_right_child_btree():
    btree: Btree = split_btree_1()

    element: object | None = btree.delete(4)

    assert element == 4
    assert btree._get_root().get_node_contents() == [1,2,3,5]
    assert btree._get_root().get_leaf_status() == True
    assert btree.validate_invariants() == None
    del btree    

def test_delete_single_element_empty_root_btree():
    btree: Btree = split_btree_1()

    element: object | None = btree.delete(3)

    assert element == 3
    assert btree._get_root().get_node_contents() == [1,2,4,5]
    assert btree._get_root().get_leaf_status() == True
    assert btree.validate_invariants() == None
    del btree

def test_delete_single_element_first_key_root_btree():
    btree: Btree = split_btree_3()

    element: object | None = btree.delete(2)

    assert element == 2
    assert btree._get_root().get_node_contents() == [5,8]
    assert btree._get_root().get_children()[0].get_node_contents() == [0,1,3,4]
    assert btree._get_root().get_leaf_status() == False
    assert btree.validate_invariants() == None
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
    assert binary_search(node.node, 5)[1] == 4
    del node

def test_insert_till_full_btreenode():
    node: BtreeNode = BtreeNode(4)
    
    node.insert(1)
    node.insert(2)
    node.insert(3)

    assert node.insert(4) == True
    assert node.insert(5) == False
    assert binary_search(node.node, 5)[1] == 4
    del node

def test_insert_duplicate_key_btreenode():
    node: BtreeNode = BtreeNode(4)
    node.node = [1]

    with pytest.raises(Exception, match="Duplicate Key"):
        node.insert(1)