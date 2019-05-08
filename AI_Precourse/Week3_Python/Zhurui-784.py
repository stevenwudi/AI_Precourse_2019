class Solution(object):
    def letterCasePermutation(self, S):
        result = [""]
        for c in S:
            temp = []
            if c.isalpha():
                for i in result:
                    temp.append(i+c.lower())
                    temp.append(i+c.upper())
            else:
                for i in result:
                    temp.append(i+c)
            result = temp
        return result