# Btree Notes

- All leaves are of the same depth (none can be deeper than others)
- Keys dictate where to search depending on comparison outcome with value to find

- Max keys is a set value for a node (M)
- Minimum number of keys for a node is half of the max rounded down: $$\lfloor M/2 \rfloor $$

- **NOTE**: The root node ignores the minimum number of keys rule, all others must follow

## Insertion Process
1. Fill root node (sorted of course)
2. If full, make two new nodes that will be the left (less) and right (more) values, the last node (middle), will be the new root node
3. From here, add elements at the bottom-most level
4. When you encounter a full leaf node, recreate the process from step 2 and bubble up the middle node to the root or parent
5. This is a recursive process where the bottom-most node will bubble up a value that keeps splitting up parent nodes, follow same process

## Deletion Proces
1. Search the key in the tree
2. There are several cases to account for during deletion
- If you delete a key and the minimum key rule is no longer satisfied you can rotate a key from a neighboring node, (left [highest] or right [lowest]) and shift out the current separator value in the parent node with that and then pull out that separator value that was returned from the parent node