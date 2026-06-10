from typing import Any, Self

class BtreeNode:

    def __init__(
            self, 
            keys: int, 
            existing_keys: list[Any] | Any | None = None, 
            is_leaf: bool = True, 
            children: list[Self] | Self | None = None,
            parent: Self | None = None,
            ):

        # Handle a single key fed into constructor        
        # if existing_keys != None and not isinstance(existing_keys, list):
        #     existing_keys: list[T] = [existing_keys]

        self.node: list[any] = existing_keys if existing_keys != None else []
        self.children: list[Self] = children if children != None else []
        self.node_size: int = keys
        self.is_leaf: bool = is_leaf
        self.number_of_children: int = keys + 1 if is_leaf is not True else 0
        self.parent: Self | None = None

    # Insert - insert an element into the node
    # Params:
    #   item - a generic that can be compared (wip)
    #   compartor() - sorts the insertion correctly (UNUSED)
    # Returns (bool) - Are the invariants valid?
    def insert(self, item) -> bool:

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

    # Insert a child into the list of children
    # Params:
    #   child_node (BtreeNode) - child to insert from a split node
    #   index (int) - calculated index using the child_search()
    def insert_child(self, child_node: Self, index: int) -> None:
        self.children.insert(index, child_node)

    # Assigns the child node with a parent node
    # Params:
    #   parent (BtreeNode) - The node higher up the tree relative to the child (self)
    def assign_parent(self, parent: Self) -> None:
        self.parent = parent
    
    # Search - searches for the item inside the current node
    def search(self, item) -> int:
        return binary_search(self.node, item)
    
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

    def get_leaf_status(self) -> bool:
        return self.is_leaf

    # Gets the children of the node
    # Returns (list[BtreeNode]) - The children objects
    def get_children(self) -> list[Self]:
        return [*self.children]
    
    def get_parental_status(self) -> Self:
        return self.parent

    def get_size(self) -> int:
        return len(self.node)
    
    def get_node_contents(self) -> list[any]:
        return [*self.node]

    # def get_max_size(self) -> int:
    #     return self.node_size
    
    def print_node(self) -> str:
        return str(self.node)

    