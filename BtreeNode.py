class BtreeNode:

    def __init__(self, size):
        self.node: list = []
        self.size: int = 0
        self.is_leaf: bool = True 

    def insert(self, item) -> bool:

        if self.size == len(self.node):
            # Splitting nodes should be handled at Btree level
            print('Split Node Operation')
            return False

        # Empty node
        if len(self.node) == 0:
            self.node.append(item)
            return True

        # Iterate through list to find valid location   
        current_index = 0
        while self.node[current_index] <= item:
            if item != self.node[current_index]:
                current_index += 1
            else:
                print('Inserting Duplicate Key! Failed Insertion')
                return False
        self.node.insert(current_index, item)
        return True

    def get_size(self) -> int:
        return self.size

    