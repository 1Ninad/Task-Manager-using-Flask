# bst.py

class TreeNode:
    def __init__(self, title):
        self.title = title
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, title):
        if not self.root:
            self.root = TreeNode(title)
        else:
            self._insert_rec(self.root, title)

    def _insert_rec(self, node, title):
        if title < node.title:
            if node.left:
                self._insert_rec(node.left, title)
            else:
                node.left = TreeNode(title)
        else:
            if node.right:
                self._insert_rec(node.right, title)
            else:
                node.right = TreeNode(title)

    def get_suggestions(self, prefix):
        suggestions = []
        self._find_prefix(self.root, prefix, suggestions)
        return suggestions

    def _find_prefix(self, node, prefix, suggestions):
        if not node:
            return
        # Check if the current node title starts with the prefix
        if node.title.startswith(prefix):
            suggestions.append(node.title)
        
        # Traverse left and right subtrees
        self._find_prefix(node.left, prefix, suggestions)
        self._find_prefix(node.right, prefix, suggestions)
