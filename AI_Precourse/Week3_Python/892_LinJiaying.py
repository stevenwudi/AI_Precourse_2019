class Solution:
    def surfaceArea(self, grid) -> int:
        N = len(grid)
        cubes = 0
        tower = 0 #numbers of towers
        pairs = 0 #the number of the pair of the cubes nestle to each other from different tower
        for i in range( N-1 ) :
            for j in range( N-1 ):
                if grid[i][j] != 0 :
                    tower += 1
                    cubes +=  grid[i][j]
                    pairs += min(grid[i][j],grid[i][j+1]) + min(grid[i][j],grid[i+1][j])

        for i in range( N - 1):
            if grid[i][N-1] != 0 :
                tower += 1
                cubes += grid[i][N-1]
                pairs += min(grid[i][N-1], grid[i+1][N-1])

        for j in range( N - 1):
            if grid[N-1][j] != 0 :
                tower += 1
                cubes += grid[N-1][j]
                pairs += min(grid[N-1][j], grid[N-1][j+1])

        cubes += grid[N-1][N-1]

        if (grid[N-1][N-1] != 0):tower += 1

        return  4*cubes + 2*tower - 2*pairs

s = Solution()
grid = [[1,2],[3,4]]
print(s.surfaceArea(grid))