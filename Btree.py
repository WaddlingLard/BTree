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


    def output_tree(self) -> str:
        print(self.root or 'Tree is empty')

if __name__ == '__main__':
    print('Hello, World!')

    btree = Btree(4)
    btree.output_tree()
    
