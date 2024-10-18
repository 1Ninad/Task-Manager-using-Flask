class Node:
    def __init__(self, key, task):
        self.key = key
        self.task = task
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key_task):
        key, task = key_task
        if self.root is None:
            self.root = Node(key, task)
        else:
            self._insert(self.root, key, task)

    def _insert(self, current_node, key, task):
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
        """Search for tasks with titles that start with the prefix."""
        results = []
        self._search(self.root, prefix, results)
        return results

    def _search(self, current_node, prefix, results):
        if current_node:
            if current_node.key.startswith(prefix):
                results.append((current_node.key, current_node.task))
            self._search(current_node.left, prefix, results)
            self._search(current_node.right, prefix, results)

    def remove(self, key):
        """Remove a task with the given title (key) from the BST."""
        self.root = self._remove(self.root, key)

    def _remove(self, current_node, key):
        if not current_node:
            return current_node

        # If key is less go left
        if key < current_node.key:
            current_node.left = self._remove(current_node.left, key)
        # If key is greater go right
        elif key > current_node.key:
            current_node.right = self._remove(current_node.right, key)
        else:
            # Node to be deleted is found
            # case 1-no children
            if not current_node.left and not current_node.right:
                return None
            # case 2-one child
            elif not current_node.left:
                return current_node.right
            elif not current_node.right:
                return current_node.left
            # case 3-two children
            else:
                # Find the minimum value node in the right subtree
                temp = self._min_value_node(current_node.right)
                current_node.key, current_node.task = temp.key, temp.task
                current_node.right = self._remove(current_node.right, temp.key)

        return current_node

    def _min_value_node(self, node):
        """Find the node with the minimum key in a subtree."""
        current = node
        while current.left:
            current = current.left
        return current