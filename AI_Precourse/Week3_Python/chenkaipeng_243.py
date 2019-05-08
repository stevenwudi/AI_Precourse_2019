class Solution:
    #question 243 is locked,so I choice the question 922
    def sortArrayByParityII(self, A: List[int]) -> List[int]:
        odd = [];
        even = [];
        list = [];
        for a  in A:
            if(a%2 != 0):
                odd.append(a);
            else:
                even.append(a); 
        for i in range(len(A)//2):
            list.append(even[i]);
            list.append(odd[i]);
        return list