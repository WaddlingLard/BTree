from BtreeNode import BtreeNode
from search_methods import child_search as amber_alert, binary_search as search
import math

class Btree:

    def __init__(self, number_of_keys):
        self.root: BtreeNode = BtreeNode(number_of_keys)
        self.max_keys: int = number_of_keys
        self.min_keys: int = math.floor(number_of_keys / 2)

    # Finds a value in the btree
    # Params:
    #   value - item to be searched for
    # Returns (bool) - did it find it?
    def exists(self, value) -> bool:
        # Check the root for the val
        return search(self.root.get_node_contents(), value) != -1
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

        invariant_check = current_node.insert(value)

        if disable_split:
            # print('split disabled')
            return

        if not invariant_check:
            # Have to split root (What if not in root though?)

            # Keep current root? (hold left side values)
            # Make 2 more nodes (middle for new root, right for right child)
            extracted_keys: list[any] = self.root.split(self.min_keys)
            
            # Get the child nodes
            right_child: BtreeNode = BtreeNode(self.max_keys, extracted_keys[1:])
            left_child: BtreeNode = self.root
            
            # Create the parent node
            new_root: BtreeNode = BtreeNode(self.max_keys, extracted_keys[:1], False, [left_child, right_child])

            # Set the new parent node
            self.root = new_root

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