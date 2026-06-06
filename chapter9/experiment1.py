# 导入 numpy 包
import numpy as np

# 定义矩阵类型判断函数
def check_type(a):
    a = np.array(a)
    s = np.eye(a.shape[0], a.shape[1])
    if (a >= s).all() and (a.T == a).all():
        return "模糊自反矩阵、模糊对称矩阵"
    elif (a >= s).all():
        return "模糊自反矩阵"
    elif (a.T == a).all():
        return "模糊对称矩阵"
    elif (hecheng(a, a) <= a).all():
        return "模糊传递矩阵"
    else:
        return "一般模糊矩阵"

# 定义判断两个矩阵是否相等的函数
def isequal(a,b):
    # 判断模糊矩阵 a,b 是否相等
    a,b = np.array(a),np.array(b)
    if (a==b).all():
        print("相等")
    else:
        print("不相等")

# 定义两个模糊矩阵的并运算函数
def bing(a,b):
    # 求模糊矩阵 a 和模糊矩阵 b 的并
    a,b = np.array(a),np.array(b)
    c = np.fmax(a,b) # 元素级的最大值计算
    return c

# 定义两个模糊矩阵的交运算函数
def jiao(a,b):
    # 求模糊矩阵 a 和模糊矩阵 b 的交
    a,b = np.array(a),np.array(b)
    c = np.fmin(a,b) # 元素级的最小值计算
    return c

# 定义一个模糊矩阵的补运算函数
def bu(a):
    # 求模糊矩阵 a 的补
    a = np.array(a)
    c = 1 - a # 元素级的计算
    return c

# 定义两个模糊矩阵的合成运算函数
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

# 实验 2 相关（合成运算计算子女与祖父母的相似程度）
# 导入 numpy 包（已在上方导入）
# 定义两个模糊矩阵的合成运算函数（已在上方定义）