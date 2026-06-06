import numpy as np
def hecheng(a,b):
    # 求模糊矩阵 a 和模糊矩阵 b 的合成
    a,b = np.array(a),np.array(b)
    if a.shape[1] == b.shape[0]:
        c = np.zeros_like(a.dot(b))
        for i in range(a.shape[0]): # 遍历 a 的行元素
            for j in range(b.shape[1]): # 遍历 b 的列元素
                empty = []
                for k in range(a.shape[1]):
                    empty.append(min(a[i,k],b[k,j])) # 行列元素比小
                c[i,j] = max(empty) # 比小结果取大
        return c
    else:
        print("输入矩阵不能做合成运算！\n请检查矩阵的维度！")