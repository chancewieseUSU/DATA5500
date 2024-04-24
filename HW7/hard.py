'''
    Deleting a node from a binary search tree involves a few steps. 
Depending on the structure of the tree and node, it may vary how 
the node is deleted. Because it is a binary search tree, each node 
has two children at most. Additionally, all nodes in its left subtree 
have values less than the node, and all nodes in its right subtree 
have values greater than the node. Generally, deleting a node from 
a binary search tree can be broken down into three different cases: 
Deleting a node with no children, one child, or two children.

Deleting Nodes:
    Deleting a node with no children is the easiest case. If the node 
has no children, it can be removed from the tree by updating the 
parent’s reference to ‘None.’ This will remove it and its values 
from the tree. 
    Deleting a node with one child is a little more complicated. 
When deleting a node with one child, we have to ensure that the 
child of the node is linked correctly to it (the parent). We can 
replace the node to be deleted with its child. For example, if we 
need to delete a node that is a left child, and it has a left child 
itself, then we move that left child up to be in place of the node 
we want to delete. Then eventually we can delete the node we wanted to.
    Deleting a node with 2 children becomes more complex, but works very 
similarly to the last case. We need to find either the smallest node 
in the right subtree (inorder successor) or largest node in the left 
subtree (inorder predecessor). We then replace the node to be deleted, 
with either the inorder successor or predecessor.
    
Edge Cases:
    One edge case is deleting the root node. When you delete the root 
note, you have to reassign the root of the tree after you delete it. 
You may have to update the root to its left or right child.
    Another edge case is deleting a non-existent node. This isn’t much 
of a problem, but we have to prepare for when a deletion request is 
made and that node doesn’t exist. We need to ignore the request or 
spit out an error message.
    One last challenge is maintaining the binary search tree property. 
When you delete a node, it’s crucial to ensure that the resulting 
tree still stays a binary search tree, so you have to be careful with 
values and variables. You have to make sure you are correctly linking 
parent nodes to their children and maintaining order. If you are 
reassigning nodes or adding them out of order, it can mess up the 
entire tree. 

'''

