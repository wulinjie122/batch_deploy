names = ['Michael', 'Bob', 'Tracy']
for name in names:
    print(name)

sum = 0
for x in range(101):
    sum = sum + x
print(sum)

arr1 = list(range(5))
print(arr1)

sum1 = 0
n = 99
while n > 0:
    sum1 = sum1 + n
    n = n - 2
print(sum1)

n1 = 1
while n1 <= 100:
    if n1 > 10: # 当n = 11时，条件满足，执行break语句
        break # break语句会结束当前循环
    print(n1)
    n1 = n1 + 1
print('END')

# 打印Bob的成绩
d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
print(d['Bob'])
d['Adam'] = 67
print(d['Adam'])

ifExists = 'Adams' in d
print(ifExists)

print(d.get('Adams', 'Default'))

d.pop('Adam')
print(d)

s1 = set([1, 2, 3])
s2 = set([2, 3, 4])
print(s1 & s2)
print(s1 | s2)

a = ['c', 'b', 'a']
a.sort()
print(a)

a = 'abc'
print(a.replace('a', 'A'))
print(a)
