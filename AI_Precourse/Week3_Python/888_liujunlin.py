class Solution:
    def fairCandySwap(self, A: List[int], B: List[int]) -> List[int]:
        sum1 = sum(A)
        sum2 = sum(B)
        diff = (sum2 - sum1) / 2
        sb = set(B)
        for a in A:
            k = a + diff
            if k in sb:
                return [a, k]
        return []
import cv2