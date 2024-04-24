class TreeNode: #creates tree - more notes on easy.py
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

def insert(root, key):  #creates insert - more notes on easy.py
    if root is None:
        return TreeNode(key)
    else:
        if key < root.key:
            root.left = insert(root.left, key)
        else:
            root.right = insert(root.right, key)
    return root
    
def search(root, key):      #creates search function
    if root is None:        #if we get to where it should be and it's not there, then it's not in the tree
        print(key,"not found in the tree.")
        return False        #return false
    if root.key == key:     #if it finds it where it should be
        print(key, "found in the tree.")
        return True         #return true
    elif key < root.key:    #if it hasn't found it yet but there's more to search, rerun
        return search(root.left, key)
    else:
        return search(root.right, key)

    
# sets list of keys
lst = [82, 45, 9, 57, 47, 46, 80, 95, 78, 31, 
        99, 72, 49, 67, 34, 56, 4, 54, 9, 42]
tree = None     # initializes tree
for i in lst:       # creates tree
    tree = insert(tree, i)

# searches values
search(tree, 9)
search(tree, 56)
search(tree, 100)