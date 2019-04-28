S = input("输入字符串")
S = list(S)
l = []
for s in S:
    if s.isalpha():
        l.append(s)
r = l[::-1]
for i in range(len(S)):
    if not S[i].isalpha():
        r.insert(i, S[i])
print(''.join(r))