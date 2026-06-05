class BtreeNode:

    def __init__(self, size):
        self.node: list = []
        self.size: int = 0
        self.is_leaf: bool = True 

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
                return False 
        self.node.insert(current_index, item)

        # Do we need to split?
        return self.node_size > len(self.node)

    def get_size(self) -> int:
        return self.size

    