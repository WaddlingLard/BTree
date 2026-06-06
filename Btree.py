from BtreeNode import BtreeNode
from binary_search import binary_search as search
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

    def insert(self, value, disable_split: bool = False):

        # Insertion should look for deepest node
        invariant_check = self.root.insert(value) 

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

    def output_tree(self) -> str:
        print(self.root or 'Tree is empty')

if __name__ == '__main__':
    print('Hello, World!')

    btree = Btree(4)
    btree.output_tree()
    
