class Node:
    def __init__(self, key, task):
        self.key = key    # task's title
        self.task = task  
        self.left = None  # Ptr to left child
        self.right = None # Ptr to right child

class BST:
    def __init__(self):
        self.root = None 

    def insert(self, key_task):
        """Inserts a task into the BST by its title (key)."""
        key, task = key_task
        if self.root is None:
            self.root = Node(key, task)  # First task - root
        else:
            self._insert(self.root, key, task)  # recursive insertion

    def _insert(self, current_node, key, task):
        """Helper function to recursively insert the task in the correct place."""
        if key < current_node.key: 
            if current_node.left is None:
                current_node.left = Node(key, task)
            else:
                self._insert(current_node.left, key, task)
        elif key > current_node.key:  
            if current_node.right is None:
                current_node.right = Node(key, task)
            else:
                self._insert(current_node.right, key, task)

    def search(self, prefix):
        """Search for tasks whose titles start with the given prefix."""
        results = []
        self._search(self.root, prefix, results)
        return results

    def _search(self, current_node, prefix, results):
        """Helper function to recursively search for matching tasks."""
        if current_node:
            if current_node.key.startswith(prefix):  # if title matches prefix
                results.append((current_node.key, current_node.task))  
            self._search(current_node.left, prefix, results)  # search left subtree
            self._search(current_node.right, prefix, results)

    def remove(self, key):
        """Remove a task by its title (key) from the BST."""
        self.root = self._remove(self.root, key)

    def _remove(self, current_node, key):
        """Helper function to recursively remove a task by its title (key)."""
        if current_node is None:
            return None
        
        # Traverse the tree to find the node to delete
        if key < current_node.key:
            current_node.left = self._remove(current_node.left, key)
        elif key > current_node.key:
            current_node.right = self._remove(current_node.right, key)
        else:
            # Node with only one child or no child
            if current_node.left is None:
                return current_node.right
            elif current_node.right is None:
                return current_node.left
            
            # Node with two children: get the inorder successor (smallest in the right subtree)
            temp = self._find_min(current_node.right)
            current_node.key, current_node.task = temp.key, temp.task
            current_node.right = self._remove(current_node.right, temp.key)
        
        return current_node

    def _find_min(self, node):
        """Find the node with the minimum key (leftmost child)."""
        while node.left is not None:
            node = node.left
        return node
            
              

    

