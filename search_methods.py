import math
from typing import Literal

# An implementation of binary search
def binary_search(list_of_vals, searching_for) -> int:
    
    values: list[any] = list_of_vals
    
    upper = len(values) - 1
    lower = 0

    while True:

        middle = math.floor((upper + lower) / 2)
        if (upper < lower):
            return -1
        elif(values[middle] == searching_for):
            return middle
        elif(values[middle] > searching_for):
            # Search Bottom Half
            upper = middle - 1       
        else:
            # Search Top Half
            lower = middle + 1

# Uses the strategy of binary search, but uses a theoretical value as
# a comparison in order to find out the child node path
# Params:
#   list_of_vals (list[any]) - The values contained in the node
#   value_to_insert (any) - The value that will be inserted into the tree (is comparable)
# Returns (int) - the index of the child for the child list
def child_search(list_of_vals: list[any], value_to_insert: any):
    
    values: list[any] = list_of_vals

    upper: int = len(values) - 1
    middle: int = 0
    lower: int = 0
    relation: Literal['lt', 'gt'] | None = None

    # Used to keep track of current status of middle for child index calc
    prev_middle: int = 0

    while True:
        middle = math.floor((upper + lower) / 2)
        if (upper < lower):
            break
        # Unneeded because duplicates will never be found
        # Idk maybe I'll throw an error if this ever happens just in case
        elif (values[middle] == value_to_insert):
            raise Exception('Error: Found item attempting to insert!')
            # return middle
        elif (values[middle] < value_to_insert):
            lower = middle + 1
            relation = 'gt'
        else:
            upper = middle - 1 
            relation = 'lt'

        prev_middle = middle

    # Work done on white board, TLDR: depending on the last relation discovered
    # it will determine the child index relative to the key index.
    # Greater than indicates a +1 to the key index (middle)
    # and Less than is just the index itself.
    if relation == 'gt':
        return prev_middle + 1
    else:
        return prev_middle    

# if __name__ == '__main__':
#     numbers = [1,2,3,4,5,6,7,8,9,10]

#     print(binary_search(numbers, 7))


























