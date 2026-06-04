from BtreeNode import BtreeNode
import math

class Btree:

    def __init__(self, number_of_keys):
        self.root: BtreeNode = BtreeNode(number_of_keys)
        self.max_keys: int = number_of_keys
        self.min_keys: int = math.floor(number_of_keys / 2)

    def insert(self, value):
        pass

    def output_tree(self) -> str:
        print(self.root or 'Tree is empty')

if __name__ == '__main__':
    print('Hello, World!')

    btree = Btree(4)
    btree.output_tree()
    
