import numpy as np
# Definition for a QuadTree node.
class Node(object):
    def __init__(self, val, isLeaf, TopLeft, TopRight, BottomLeft, BottomRight):
        self.val = val
        self.isLeaf = isLeaf
        self.TopLeft = TopLeft
        self.TopRight = TopRight
        self.BottomLeft = BottomLeft
        self.BottomRight = BottomRight

class Solution(object):
    def construct(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: Node
        """
        N = len(grid)
        if N == 1:
            return Node(grid[0][0] == 1, True, None, None, None, None)
        mid=int(N/2)
        TopLeftSum = sum(sum(grid[0:mid,0:mid]))
        TopRightSum = sum(sum(grid[0:mid,mid:N]))
        BottomLeftSum = sum(sum(grid[mid:N,0:mid]))
        BottomRightSum = sum(sum(grid[mid:N,mid:N]))
        node = Node(False, False, None, None, None, None)
        if TopLeftSum == TopRightSum == BottomLeftSum == BottomRightSum:
            if TopLeftSum == 0:
                node.isLeaf = True
                node.val = False
            elif TopLeftSum == (N / 2) ** 2:
                node.isLeaf = True
                node.val = True
        if node.isLeaf:
            return node
        node.val = '*'
        
        node.TopLeft = self.construct(grid=grid[0:mid,0:mid])
        node.TopRight = self.construct(grid=grid[0:mid,mid:N])
        node.BottomLeft = self.construct(grid=grid[mid:N,0:mid])
        node.BottomRight = self.construct(grid=grid[mid:N,mid:N])
        return node
    def Print(self,node):#Depth-first search.
        print('node:isLeaf = {0},val = {1}'.format(node.isLeaf,node.val))
        if node.TopLeft:
            self.Print(node.TopLeft)
        if node.TopRight:
            self.Print(node.TopRight)
        if node.BottomLeft:
            self.Print(node.BottomLeft)
        if node.BottomRight:
            self.Print(node.BottomRight)
    
grid=np.array([[1,1,1,1,0,0,0,0],[1,1,1,1,0,0,0,0],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,0,0,0,0],\
    [1,1,1,1,0,0,0,0],[1,1,1,1,0,0,0,0],[1,1,1,1,0,0,0,0]])
solution=Solution()
node=solution.construct(grid=grid)
print('Depth-first search:')
solution.Print(node=node)
