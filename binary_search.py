import math

# An implementation of binary search
def binary_search(list_of_vals, searching_for) -> int:
    
    values: list[any] = list_of_vals
    
    upper = len(values) - 1
    lower = 0
    
    while True:

        # Edge Case: Singleton
        if len(values) == 1:
            return 0 if values[0] == searching_for else -1

        middle = math.floor((upper + lower) / 2)
        if (upper < lower):
            return -1
        elif(values[middle] == searching_for):
            return middle
        elif(values[middle] > searching_for):
            # Search Bottom Half
            upper = middle - 1       
        else:
            lower = middle + 1
            # Search Top Half
            # if len(values) <= 2:
            #     # Edge case: 1-2 element lists
            #     lower += 1

if __name__ == '__main__':
    numbers = [1,2,3,4,5,6,7,8,9,10]

    print(binary_search(numbers, 7))