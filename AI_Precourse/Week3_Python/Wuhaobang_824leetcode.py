class Solution:
    def toGoatLatin(self, S: str) -> str:
        list = S.split(" ")
        #print(list[0][0])
        lsize = len(list)
        for i in range(0,lsize):
            if  list[i][0] in 'aeiouAEIOU' :
                list[i] += 'ma'
            else :
                list[i] = list[i][1:]+list[i][:1]
                list[i] +='ma'
            for j in range(0,i+1):
                list[i] += 'a'
        rstr=""
        for i in range(0,lsize-1):
            rstr += list[i]
            rstr += " "
        rstr +=list[lsize-1]
        return rstr