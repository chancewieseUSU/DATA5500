from print_tree import *    #brings in code for display function at the end

class TreeNode:     #class for creating tree
    def __init__(self, key):
        self.key = key      #initializes values for each root/node
        self.left = None
        self.right = None

def insert(root, key):      #creates insert function
    if root is None:        
        return TreeNode(key)    #if its new, set the new root/node
    if key < root.key:      #if the key is less than the current root key, move it to the left
        root.left = insert(root.left, key)
    else:   #if key not less than, it puts key to the right
        root.right = insert(root.right, key)
    return root
    
    

#sets list of keys
lst = [50, 45, 9, 57, 47, 46, 80, 95, 78, 31, 
        99, 72, 49, 67, 34, 56, 4, 54, 9, 42]
#initializes tree
tree = None
#creates tree
for i in lst:
    tree = insert(tree, i)
#displays tree - took from week8_trees
display(tree)   #displays tree

