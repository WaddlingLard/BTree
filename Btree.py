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

        # Ensure the tree already doesn't contain the element
        if self.exists(value) != None:
            # Already has element
            print('Key is already present in the Btree!')
            return

        while not current_node.get_leaf_status():

            # Retrieve the children of that node
            child_nodes: list[BtreeNode] = current_node.get_children()

            # Must have child nodes so we are going to find the index where it is
            search_result: tuple[SearchResult, int] = amber_alert(current_node.get_node_contents(), value)
            result, child_index = search_result

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

    
    # This is going to be a tricky method, many cases to account for and recursion is likely
    def delete(self, key: object) -> object:

        # Locate which node contains the value
        node_location: BtreeNode = self.exists(key)
        
        if node_location == None:
            print("Key doesn't exist in the Btree!")
            return None

        key: object
        deleted_at_index: int

        # Simple deletion for now
        deleted_key: tuple[object, int] = node_location.delete(key)
        key, deleted_at_index = deleted_key


        violation: tuple[BtreeNode, list[InvariantCheck]] | None = self.validate_invariants()

        # Deletion didn't mess up the tree. Yay!
        if violation == None:
            return key
        
        violated_node: BtreeNode
        violation_types: list[InvariantCheck]

        # What if violation of keys and children?
        while violation != None:
            
            violated_node, violation_types = violation

            # Basic strategy of dealing with a violation [if a child] (InvariantCheck.KEY)
            # A) Merge parent
            # B) Merge with neighboring child (most inwards, does that make sense?)
            # C) Set as root
            index: int = 0
            parent_node: BtreeNode | None = violated_node.get_parent()
            
            if parent_node == None:
                # We are at the root, NOTE: have to consider inner nodes too
                # A) Pull key from child, need to account for deeper levels
                root_children: list[BtreeNode] = violated_node.get_children()

                lchild_of_del_key: BtreeNode = root_children[deleted_at_index]
                rchild_of_del_key: BtreeNode = root_children[deleted_at_index + 1]

                shifted_key: object = lchild_of_del_key.delete_at(lchild_of_del_key.get_size() - 1)
                violated_node.insert(shifted_key)

            else:
                child_nodes: list[BtreeNode] = parent_node.get_children()
                for i, child_node in enumerate(child_nodes):
                    if violated_node == child_node:
                        index = i
                        break
                
                # Will grab the child 'left' to it if the current index 
                # is above the middle (math.floor(children / 2)), else 'right'
                neighb_location: NodeLocation = NodeLocation.LEFT if index >= math.floor(len(child_nodes) / 2) else NodeLocation.RIGHT
                # print(neighb_location.value)
                neighbor_node: BtreeNode = child_nodes[index + neighb_location.value]
                
                # Execute the merges
                violated_node.merge(parent_node, neighb_location)
                violated_node.merge(neighbor_node, neighb_location)

                # Delete the previous nodes and do proper root reassignment case
                if parent_node == self.root:
                    self.root = violated_node
                
                del parent_node
                del neighbor_node

            # Check to see if new violation occurred
            violation = self.validate_invariants()

        return key

    # A handy method to validate all invariants for the Btree
    # and it will return the fussy BtreeNode that is violating the constraint
    # NOTE: Should this account for multiple violations? Is that even possible?

        invariant_checks: set = set([InvariantCheck.CHILDREN, InvariantCheck.KEYS, InvariantCheck.SORT])

        def sort_check(items: list[object], prev_value: object) -> bool:
            if len(items) == 1:
                return True
            elif prev_value > items[0]:
                return False
            else:
                return sort_check(items[1:], items[0])

        sort_rule: Callable[[BtreeNode], bool] = lambda node: len(node.get_node_contents()) == 0 or sort_check(node.get_node_contents(), node.get_node_contents()[0]) 

        node_level: int = 0
        lowest_level: int | None = None

        queue: list[tuple[BtreeNode, int]] = [(self.root, node_level)]
        buffer: list[BtreeNode] = []
        type_of_node: NodeType = NodeType.UNKNOWN
        rule_book: dict[NodeType, dict[InvariantCheck, list[Callable[[BtreeNode], bool]]]] = { 
            NodeType.LEAF: {
                InvariantCheck.CHILDREN: [lambda node: len(node.get_children()) == 0],
                InvariantCheck.KEYS: [lambda node: self.max_keys >= len(node.get_node_contents()) >= math.ceil(self.max_keys / 2)],
                InvariantCheck.SORT: [sort_rule]
            },
            NodeType.ROOT: {
                InvariantCheck.CHILDREN: [
                    lambda node: node.get_leaf_status() and len(node.get_children()) == 0, 
                    lambda node: not node.get_leaf_status() and self.max_keys + 1 >= len(node.get_children()) >= 2
                    ],
                InvariantCheck.KEYS: [
                    lambda node: node.get_leaf_status() and self.max_keys >= len(node.get_node_contents()) >= 0,
                    lambda node: not node.get_leaf_status() and self.max_keys >= len(node.get_node_contents()) >= 1],
                InvariantCheck.SORT: [sort_rule]
            },
            NodeType.INNER: {
                InvariantCheck.CHILDREN: [lambda node: self.max_keys + 1 >= len(node.get_children()) >= math.floor(self.max_keys / 2) + 1],
                InvariantCheck.KEYS: [lambda node: self.max_keys >= len(node.get_node_contents()) >= math.floor(self.max_keys / 2)],
                InvariantCheck.SORT: [sort_rule]
            }
            # NodeType.UNKNOWN: {}
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
                # Root can also be setting the lowest_level invar check
                lowest_level = current_node_level if is_leaf else None
                type_of_node = NodeType.ROOT
            elif not is_leaf and current_node.get_parental_status() != None:
                type_of_node = NodeType.INNER
            elif is_leaf:
                lowest_level = current_node_level if lowest_level == None else lowest_level
                type_of_node = NodeType.LEAF

            # Validate the node
            # Type is messy but it is just a key -> list of lambdas
            rules: dict[InvariantCheck, list[Callable[[BtreeNode], bool]] | Callable[[BtreeNode], bool]] = rule_book[type_of_node]
            # checks: list[bool | list[bool]] = [[check(current_node) for check in rules[rule]] for rule in rules if isinstance(rules[rule], list)] 


            # Pretty cool nested comprehension, you can get a filtered result using the ':=' operator to call the lambda and only return a specific value
            # checks: list[list[bool]] = [[result for check in rules[rule] if (result := check(current_node) == True)] for rule in rules]
            checks: list[list[InvariantCheck]] = [[rule for check in rules[rule] if check(current_node) == True] for rule in rules]
            aggregated_checks: list[InvariantCheck] = [result for sublist in checks for result in sublist]

            if len(set([InvariantCheck.CHILDREN, InvariantCheck.KEYS]) & set(aggregated_checks)) != 2 or (is_leaf and current_node_level != lowest_level):
                # print('Satified these conditions:', aggregated_checks)
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