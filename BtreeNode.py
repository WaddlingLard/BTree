from typing import Any, Self, Callable, Literal
from enum import Enum
from search_methods import binary_search, child_search, SearchResult

class NodeLocation(Enum):
    RIGHT = 1
    LEFT = -1

class BtreeNode:

    def __init__(
            self, 
            keys: int, 
            existing_keys: list[object] | object | None = None, 
            is_leaf: bool = True, 
            children: list[Self] | Self | None = None,
            parent: Self | None = None,
            ):

        # Handle a single key fed into constructor        
        # if existing_keys != None and not isinstance(existing_keys, list):
        #     existing_keys: list[T] = [existing_keys]

        self.node: list[object] = existing_keys if existing_keys != None else []
        self.children: list[Self] = children if children != None else []
        self.node_size: int = keys
        self.leaf_status: bool = is_leaf
        self.number_of_children: int = keys + 1 if is_leaf is not True else 0
        self.parent: Self | None = None

    # Insert - insert an element into the node
    # Params:
    #   item - a generic that can be compared (wip)
    #   location_bypass - providing a location circumvents the whole process and immediatly appends to
    #   the respective location LEFT <- [collection] -> RIGHT
    #   compartor() - sorts the insertion correctly (UNUSED)
    # Returns (bool) - Are the invariants valid?
    def insert(self, item: object | list[object]) -> bool:

        # Size check, cannot add more than limit but should consider to handle in Btree instead of here
        # if self.node_size == len(self.node):
        #     # Splitting nodes should be handled at Btree level
        #     print('Split Node Operation')
        #     return False

        # Empty node
        # if len(self.node) == 0:
        #     self.node.append(item)
        #     return False

        # Iterate through list to find valid location   
        current_index = 0
        while current_index < len(self.node) and self.node[current_index] <= item:
            if item != self.node[current_index]:
                current_index += 1
            else:
                # Maybe implement proper error handling, but for now its sufficient 
                print('Inserting Duplicate Key! Failed Insertion')
                raise Exception('Error: Duplicate Key')
        self.node.insert(current_index, item)

        # Do we need to split?
        return self.node_size >= len(self.node)

    # Finds the key and "deletes" it
    # Params:
    #   item (object) - The item to be deleted
    # Returns tuple[object, int] - The "deleted" item paired with its index
    def delete(self, item: object) -> tuple[object, int]:
        index_location: int = self.search(binary_search, item)[1]
        return self.node.pop(index_location), index_location

    #
    def delete_at(self, index: int) -> object:
        return self.node.pop(index)

    # Insert a child into the list of children
    # Params:
    #   child_node (BtreeNode) - child to insert from a split node
    #   index (int) - calculated index using the child_search()
    def insert_child(self, child_node: Self, index: int) -> None:
        self.children.insert(index, child_node)

    # Merge with another node, children and all
    # Params:
    #   merging_node (BtreeNode) - the merger
    def merge_neighbor(self, merging_node: Self, relative_position: NodeLocation):
        if relative_position == NodeLocation.LEFT:
            merging_node_contents: list[object] = merging_node.get_keys()
            self_contents: list[object] = self.get_keys()

            self.node = [*merging_node_contents, *self_contents]
        else:
            self.node.extend(merging_node.get_keys().copy())

        # Flatten the list
        # def flatten(node_list: list[list[object] | object]):

    # Merges the parent by grabbing the key that is respective to the child node
    def merge_parent(self, parent_node: Self, child_neighb_location: NodeLocation):
        children: list[Self] = parent_node.get_children()
        parent_key: object | None = None
        for index, child in enumerate(children):
            if self == child:

                # NOTE: MUST CONSIDER DIFFERENT RELATIVE LOCATIONS FOR THE KEY IN RELATION TO NEIGHBOR POSITIONING
                parent_key = parent_node.delete_at(index + (0 if child_neighb_location == NodeLocation.RIGHT else -1))
                parent_node.evict_child(index + child_neighb_location.value)
                break

        if child_neighb_location == NodeLocation.LEFT:
            # Append parent_key to the front of the node
            self.node.insert(0, parent_key)
        else:
            self.node.append(parent_key)

    def evict_child(self, index: int) -> Self:
        return self.children.pop(index)

    # Assigns the child node with a parent node
    # Params:
    #   parent (BtreeNode) - The node higher up the tree relative to the child (self)
    def assign_parent(self, parent: Self) -> None:
        self.parent = parent
    
    # Search - searches for the item inside the current node
    # Params:
    #   search_method (Callable[[list[any], object], int]) - generic search that takes in a list and an item to search for
    #   item (object) - item to be searched for
    # Returns tuple[SearchResult, int] - the search result and the index corresponding to that result
    def search(
            self, 
            search_method: Callable[[list[any], object], int], 
            item: object,
            **additional_params
            ) -> tuple[SearchResult, int]:
        return search_method(self.node, item, **additional_params)
    
    # Split the node with a provided range
    # Params:
    #   range - inclusive range of indexes that will be extracted
    # Returns (list[any]) - the elements that will be repacked into a new node   
    def split(self, start_index: int) -> list[any]:
        values_to_extract: list[any] = [*self.node[start_index:]]
        self.node = self.node[:start_index]
        return values_to_extract
    
    # Split the children with a provided range (signed by a judge)
    # Params:
    #   range - inclusive range of indexes that will be extracted
    # Returns (list[BtreeNode]) - the nodes that will be rehomed into a new node
    def split_children(self, start_index: int) -> list[any]:
        children_to_extract: list[Self] = [*self.children[start_index:]]
        self.children = self.children[:start_index]
        return children_to_extract

    def is_leaf(self) -> bool:
        return self.leaf_status

    # Gets the children of the node
    # Returns (list[BtreeNode]) - The children objects
    def get_children(self) -> list[Self]:
        return self.children

    # Gets a specific child via the index
    # Returns BtreeNode - The child
    def get_child(self, index: int) -> Self:
        return self.children[index]
    
    # def get_head_key(self) -> object:
    #     return len(self.node) == 0 and self.node[0] or self.node[len(self.node) - 1]

    def get_parent(self) -> Self | None:
        return self.parent

    def get_size(self) -> int:
        return len(self.node)
    
    def get_keys(self) -> list[Any]:
        return [*self.node.copy()]

    def curr_size(self) -> int:
        return len(self.node)
    
    def cldrn_size(self) -> int:
        return len(self.children)

    def get_key(self, index: int) -> object | None:
        if index > len(self.node) - 1:
            return None
        return self.node[index]

    # def get_max_size(self) -> int:
    #     return self.node_size
    
    def print_node(self) -> str:
        return str(self.node)

    