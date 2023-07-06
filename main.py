from Board import *

a = np.zeros((4,4),dtype=int)
print(type(a))
a[0,0] = 1
a[1,1] = 2
a[2,2] = 3
a[3,3] = 4



b = np.array([[1,4,3,4,4,7,3,1,5],[1,3,5,7,4,8,4,2,5],[2,4,7,1,4,7,9,3,2],[1,1,2,4,4,7,3,1,5],[1,3,5,7,4,8,4,2,5],[1,4,3,1,4,7,9,3,2],[1,4,3,4,4,7,3,1,5],[1,3,5,7,4,4,4,2,5],[2,4,7,1,4,7,9,3,2]])

for row in b:
    print(len(np.unique(row))==len(row))

print(b)
for x in range(9):
    square = b[x // 3 * 3:x // 3 * 3 + 3, x % 3 * 3:x % 3 * 3 + 3]
    print(square)

a = Board()
a.print_board()
