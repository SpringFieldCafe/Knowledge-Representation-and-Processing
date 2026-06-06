import numpy as np


# =========================
# 1. 判断是否为模糊矩阵
# =========================
def is_fuzzy_matrix(a):
    """
    判断矩阵元素是否都在 [0, 1] 之间
    """
    a = np.array(a, dtype=float)
    return np.all(a >= 0) and np.all(a <= 1)


# =========================
# 2. 判断模糊矩阵类型
# =========================
def check_type(a):
    """
    判断模糊矩阵的类型：
    1. 自反模糊矩阵：主对角线元素都为 1
    2. 反自反模糊矩阵：主对角线元素都为 0
    3. 对称模糊矩阵：A = A.T
    4. 传递模糊矩阵：A ∘ A <= A
    """

    a = np.array(a, dtype=float)

    if not is_fuzzy_matrix(a):
        return "不是模糊矩阵"

    if a.shape[0] != a.shape[1]:
        return "一般模糊矩阵"

    n = a.shape[0]
    diag = np.diag(a)

    result = []

    # 判断自反
    if np.all(diag == 1):
        result.append("自反模糊矩阵")

    # 判断反自反
    if np.all(diag == 0):
        result.append("反自反模糊矩阵")

    # 判断对称
    if np.all(a.T == a):
        result.append("对称模糊矩阵")

    # 判断传递
    aa = hecheng(a, a)
    if np.all(aa <= a):
        result.append("传递模糊矩阵")

    if len(result) == 0:
        result.append("一般模糊矩阵")

    return "，".join(result)


# =========================
# 3. 判断两个模糊矩阵是否相等
# =========================
def isequal(a, b):
    """
    判断两个模糊矩阵是否相等
    """
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)

    if a.shape != b.shape:
        print("两个矩阵维度不同，不相等")
        return False

    if np.all(a == b):
        print("相等")
        return True
    else:
        print("不相等")
        return False


# =========================
# 4. 模糊矩阵的并运算
# =========================
def bing(a, b):
    """
    模糊矩阵的并：
    对应元素取最大值
    """
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)

    if a.shape != b.shape:
        raise ValueError("两个矩阵维度不同，不能做并运算")

    return np.maximum(a, b)


# =========================
# 5. 模糊矩阵的交运算
# =========================
def jiao(a, b):
    """
    模糊矩阵的交：
    对应元素取最小值
    """
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)

    if a.shape != b.shape:
        raise ValueError("两个矩阵维度不同，不能做交运算")

    return np.minimum(a, b)


# =========================
# 6. 模糊矩阵的补运算
# =========================
def bu(a):
    """
    模糊矩阵的补：
    每个元素用 1 减去原元素
    """
    a = np.array(a, dtype=float)

    if not is_fuzzy_matrix(a):
        raise ValueError("输入不是模糊矩阵")

    return 1 - a


# =========================
# 7. 模糊矩阵的合成运算
# =========================
def hecheng(a, b):
    """
    模糊矩阵的合成：
    C = A ∘ B

    计算规则：
    c[i][j] = max( min(a[i][k], b[k][j]) )
    """

    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)

    if a.shape[1] != b.shape[0]:
        raise ValueError("A 的列数必须等于 B 的行数，才能进行模糊矩阵合成")

    row = a.shape[0]
    col = b.shape[1]
    mid = a.shape[1]

    c = np.zeros((row, col))

    for i in range(row):
        for j in range(col):
            temp = []
            for k in range(mid):
                temp.append(min(a[i][k], b[k][j]))
            c[i][j] = max(temp)

    return c


# =========================
# 8. 打印矩阵
# =========================
def print_matrix(name, matrix):
    print(name)
    print(np.array(matrix))
    print()


# =========================
# 实验 1
# =========================
def experiment_1():
    print("========== 实验 1：模糊矩阵基本运算 ==========")

    a = [
        [1, 0.87, 0.5, 0],
        [0.34, 0.63, 0.98, 0.2],
        [0.56, 0.21, 0.25, 0.5],
        [0.4, 0.36, 0.64, 0.9]
    ]

    b = [
        [0.99, 0.87, 1, 0],
        [0.34, 1, 0.98, 0.2],
        [1, 0.87, 0.32, 0.7],
        [0.4, 0.78, 0.54, 1]
    ]

    print_matrix("输入矩阵 a：", a)
    print_matrix("输入矩阵 b：", b)

    print("判断模糊矩阵 a 的类型：")
    print(check_type(a))
    print()

    print("判断模糊矩阵 b 的类型：")
    print(check_type(b))
    print()

    print("判断模糊矩阵 a、b 是否相等：")
    isequal(a, b)
    print()

    print_matrix("求模糊矩阵 a 和模糊矩阵 b 的并：", bing(a, b))
    print_matrix("求模糊矩阵 a 和模糊矩阵 b 的交：", jiao(a, b))
    print_matrix("求模糊矩阵 a 的补：", bu(a))
    print_matrix("求模糊矩阵 a 和模糊矩阵 b 的合成：", hecheng(a, b))


# =========================
# 实验 2
# =========================
def experiment_2():
    print("========== 实验 2：子女与祖父母相似程度 ==========")

    # R 表示子女与父母的相似关系
    # 行：子、女
    # 列：父、母
    R = [
        [0.2, 0.8],
        [0.6, 0.1]
    ]

    # S 表示父母与祖父母的相似关系
    # 行：父、母
    # 列：祖父、祖母
    S = [
        [0.5, 0.7],
        [0.1, 0]
    ]

    print_matrix("子女与父母的相似关系矩阵 R：", R)
    print_matrix("父母与祖父母的相似关系矩阵 S：", S)

    result = hecheng(R, S)

    print_matrix("子女与祖父母的相似关系矩阵 R o S：", result)

    print("结果解释：")
    print("第 1 行表示儿子与祖父、祖母的相似程度")
    print("第 2 行表示女儿与祖父、祖母的相似程度")
    print()
    print("所以：")
    print("儿子与祖父的相似程度为：", result[0][0])
    print("儿子与祖母的相似程度为：", result[0][1])
    print("女儿与祖父的相似程度为：", result[1][0])
    print("女儿与祖母的相似程度为：", result[1][1])


# =========================
# 主函数
# =========================
if __name__ == "__main__":
    experiment_1()
    experiment_2()