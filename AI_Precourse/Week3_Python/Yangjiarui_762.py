# Prime Number of Set Bits in Binary Representation
class Solution:
    def countPrimeSetBits(self, L: int, R: int) -> int:
        ans = 0
        tup = {2, 3, 5, 7, 11, 13, 17, 19}
        for i in range(L, R+1):
            if bin(i).count("1") in tup:
                ans += 1
        return ans
