# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def averageOfLevels(self, root: TreeNode) -> List[float]:
        if root is None:
            return []
        res = []
        count = 1;
        copy_count = 1;
        next_count = 0;
        _sum = 0;
        queue = [root]
        while(len(queue)):
            node = queue.pop(0)
            count = count - 1
            _sum = _sum + node.val
            if node.left is not None:
                queue.append(node.left)
                next_count = next_count + 1
            if node.right is not None:
                queue.append(node.right)
                next_count = next_count + 1
            if count == 0:
                res.append(_sum / copy_count)
                count = copy_count = next_count
                next_count = _sum = 0
        return res