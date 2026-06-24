from BtreeNode import BtreeNode
from search_methods import child_search as amber_alert, binary_search as search
import math
from typing import Literal
from collections.abc import Callable
from enum import Enum
# from string.templatelib import Template

class Btree:

    def __init__(self, number_of_keys):
        self.root: BtreeNode = BtreeNode(number_of_keys)
        self.max_keys: int = number_of_keys
        self.min_keys: int = math.floor(number_of_keys / 2)

    # Finds a value in the btree
    # Params:
    #   value - item to be searched for
    # Returns (bool) - did it find it?
    def exists(self, value) -> BtreeNode | None:
        # Check the root for the val
        current_node: BtreeNode = self.root
        
        while current_node != None:
            results: tuple[SearchResult, int] = current_node.search(amber_alert, value, ignore_hit=False)
            # print(results)
            
            search_result, index = results
            match search_result:
                case (SearchResult.FOUND_ITEM):
                    return current_node
                case (SearchResult.NOT_FOUND):
                    return None
                case (SearchResult.CHILD_LOCATED):
                    if current_node.get_leaf_status():
                        return None
                        
                    current_node = current_node.get_child(index)

        # Note: Need to alter search when it fails to find the last value it attempted searching

    # Inserts a value into the tree, handles split nodes if invariants are violated
    # Params:
    #   value (object) - Object to be inserted the tree (Should have a comparison system established)
    #   disable_split (bool) - USED FOR TESTING (Likely be removed later) Prevents splitting of nodes 
    # Returns (none) - nothing is returned (for now)
    def insert(self, value: object, disable_split: bool = False) -> None:

        # Insertion should look for deepest node
        # It is safe to make the assumption that if a key (from non-leaf node)
        # has one child, it should also have a child for the inverse relation
        # Ex: (Less Than Node) Key (Greater Than Node)
        # invariant_check = self.root.insert(value) 

        # Process of finding which path to branch
        # 1. From the root, first use a system to compare with the root to find appropriate range
        # 2. Retrieve the child that belongs down that path and:
        #   A. Repeat if not a leaf node 
        #   B. If leaf node, insert!
        # Handle splitting logic after... 
        current_node: BtreeNode = self.root

        while not current_node.get_leaf_status():

            # Retrieve the children of that node
            child_nodes: list[BtreeNode] = current_node.get_children()

            # Must have child nodes so we are going to find the index where it is
            child_index: int = amber_alert(current_node.get_node_contents(), value)
            
            current_node = child_nodes[child_index] 

        valid_invariant = current_node.insert(value)

        if valid_invariant or disable_split:
            return

        # Have to split node where invariant is violated
        # Keep current node, here's the plan
        # 1. Split the childs keys and only keep the leftmost portion of the list
        # 2. With the extracted keys, create a sibling node and bubble up the middle key
        # 3. If no more invariants violated, carry on, otherwise recursion
        while not valid_invariant:

            extracted_keys: list[any] = current_node.split(self.min_keys)
            extracted_children: list[BtreeNode] = current_node.split_children(self.min_keys) if not current_node.get_leaf_status() else []
            has_children: bool = len(extracted_children) != 0

            # Retrieve parent if exists
            parent_node: BtreeNode | None = current_node.get_parental_status()

            # If parent_node is None that means this must be the root
            # Create and prepare nodes
            left_child: BtreeNode = current_node
            right_child: BtreeNode = BtreeNode(self.max_keys, extracted_keys[1:], is_leaf=not has_children, children=extracted_children)
            
            if parent_node != None:

                # There is a parent, assign to new child
                right_child.assign_parent(parent_node)
                
                # Bubble up middle key and save new child node
                middle_key: any = extracted_keys[0]

                # Since we are always creating a right child, the index for the child node relative
                # to the key index should be +1
                valid_invariant = parent_node.insert(middle_key)
                parent_node.insert_child(right_child, parent_node.search(middle_key) + 1)            
                current_node = parent_node

            else:
                # There is no parent, make it
                new_root: BtreeNode = BtreeNode(self.max_keys, extracted_keys[:1], False, [left_child, right_child])
                parent_node = new_root

                # Assign to children
                left_child.assign_parent(parent_node)
                right_child.assign_parent(parent_node)
            
                # Set the new root node because there was no parent before this
                self.root = parent_node
                valid_invariant = True


    # A handy method to validate all invariants for the Btree
    # and it will return the fussy BtreeNode that is violating the constraint
    # NOTE: Should this account for multiple violations? Is that even possible?
    def validate_invariants(self) -> BtreeNode | None:

        class NodeType(Enum):
            ROOT = 'root',
            INNER = 'inner',
            LEAF = 'leaf',
            UNKNOWN = 'unknown'

        nonl_invari_rule: list[Callable[[BtreeNode]], bool] = [lambda node: node.get_children() and len(node.get_children()) - 1 == len(node.get_node_contents())]
        node_level: int = 0
        lowest_level: int | None = None

        queue: list[tuple[BtreeNode, int]] = [(self.root, node_level)]
        buffer: list[BtreeNode] = []
        type_of_node: NodeType = NodeType.UNKNOWN
        rule_book: dict[NodeType, list[Callable[[BtreeNode | int], bool]]] = { 
            NodeType.ROOT: [*nonl_invari_rule, lambda node: node.get_leaf_status() or len(node.get_children()) >= 2], 
            NodeType.INNER: [*nonl_invari_rule, lambda node: len(node.get_children()) > math.ceil(self.max_keys / 2)],
            NodeType.LEAF: [lambda node: len(node.get_children()) == 0],
            # NodeType.UNKNOWN: []
            }

        while len(queue) != 0:

            type_of_node = NodeType.UNKNOWN
            queued_node: tuple[BtreeNode, int] = queue.pop(0)
            current_node_level: int = queued_node[1]
            current_node: BtreeNode = queued_node[0] 
            is_leaf: bool = current_node.get_leaf_status()

            if len(current_node.get_node_contents()) > self.max_keys:
                # Key size invariant violated
                return current_node

            # Find what node it is
            if current_node == self.root:
                type_of_node = NodeType.ROOT
            elif not is_leaf and current_node.get_parental_status() != None:
                type_of_node = NodeType.INNER
            elif is_leaf:
                lowest_level = current_node_level if lowest_level == None else lowest_level
                type_of_node = NodeType.LEAF

            # Validate the node
            rules: list[Callable[[BtreeNode], bool]] = rule_book[type_of_node]
            checks: list[bool] = [rule(current_node) for rule in rules]
            
            if False in checks or (is_leaf and current_node_level != lowest_level):
                return current_node

            # Add more nodes to the buffer
            if not is_leaf:
                buffer.extend(current_node.get_children())

            if len(queue) != 0:
                continue

            # New layer of nodes
            node_level += 1
            queue.extend([(node, node_level) for node in buffer])
            buffer.clear()

    # From the root, collect all the children and return them (unsure how to do order)
    # Params:
    #   method_of_retrieval - depth or breadth
    # Returns (list[BtreeNode]) - children
    def retrieve_children(self) -> list[BtreeNode]:
        # Just getting from root, will need to implement recursive gathering
        children: list[BtreeNode] = []
        children.extend(self.root.get_children())
        return children

    def output_root(self) -> str:
        # return print(self.root.print_node())
        return self.root.print_node()

    # Outputs the whole tree, useful for debugging
    def output_tree(self) -> None:

        queue: list[BtreeNode] = [self.root]
        
        node_level: int = 0

        # Can't use templates for this :(
        # node_contents: Template = t'{[x.get_node_contents() for x in queue]}'
        # node_str: Template = t'Level: {node_level} {node_contents.interpolations[0].value}'
        
        get_node_contents: function = lambda list_of_nodes: f'{[x.get_node_contents() for x in list_of_nodes]}'
        create_node_str: function = lambda level, contents: f'{level} {contents}'

        # Holds the next layer of nodes before pushing onto the queue
        buffer: list[BtreeNode] = []

        output: str = ''

        output += f'{create_node_str(node_level, get_node_contents(queue))}\n'
        # output += f'{node_str.strings[0]} {node_str.interpolations[0].value} {node_str.interpolations[1].value}\n'

        while len(queue) != 0:
            
            current_node: BtreeNode = queue.pop(0)
            
            if not current_node.get_leaf_status():
                # Load up the buffer with the children
                buffer.extend(current_node.get_children())

            if len(queue) != 0:
                # Still more work to do
                continue

            # Apply any work from the buffer over and append the new output to the string
            queue.extend(buffer)
            buffer.clear()

            if len(queue) == 0:
                # No more work to do
                break;

            node_level += 1
            output += f'{create_node_str(node_level, get_node_contents(queue))}\n'
            # output += f'{node_str.strings[0]} {node_str.interpolations[0].value} {node_str.interpolations[1].value}\n'

        print(output)


if __name__ == '__main__':
    print('Hello, World!')

    btree = Btree(4)
    btree.insert(1)
    btree.insert(4)
    btree.insert(3)
    btree.insert(6)
    btree.insert(10)
    # btree.insert(10)
    # btree.insert(76)
    # btree.output_tree()
    btree.output_root()

    del btree