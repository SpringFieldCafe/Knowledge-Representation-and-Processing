from pyDatalog import pyDatalog

# 书上写的是 create_atoms
pyDatalog.create_atoms('N, N1, X, Y, X0, X1, X2, X3, X4, X5, X6, X7')
pyDatalog.create_atoms('ok, queens, next_queen, pred, pred2')

size = 8

# 判断两个皇后是否不冲突
ok(X1, N, X2) <= (X1 != X2) & (X1 != X2 + N) & (X1 != X2 - N)

# N 的前驱 N1 = N - 1
pred(N, N1) <= (N > 1) & (N1 == N - 1)

# 只有 1 个皇后时，可以放在 0~7 任意一行
queens(1, X) <= (X1._in(range(size))) & (X1 == X[0])

# 递归求解 N 皇后
queens(N, X) <= pred(N, N1) & queens(N1, X[:-1]) & next_queen(N, X)

# pred2 用于 next_queen 的递归
pred2(N, N1) <= (N > 2) & (N1 == N - 1)

# 当只有两个皇后时，判断两者是否冲突
next_queen(2, X) <= (X1._in(range(8))) & ok(X[0], 1, X1) & (X1 == X[1])

# 判断新皇后和之前所有皇后是否冲突
next_queen(N, X) <= pred2(N, N1) & next_queen(N1, X[1:]) & ok(X[0], N1, X[-1])

# 输出结果
print(queens(size, (X0, X1, X2, X3, X4, X5, X6, X7)))