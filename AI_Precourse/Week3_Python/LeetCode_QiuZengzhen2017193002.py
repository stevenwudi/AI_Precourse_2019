# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def invertTree(self, root):
        """
        :type root: TreeNode
        :rtype: TreeNode
        """
        # For each node, flip its left and right nodes
        if root is None:
            return root
        temp = root.right if root.right else None
        root.right = self.invertTree(root.left)
        root.left = self.invertTree(temp)
        return root