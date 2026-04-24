class animal(object):
    def __init__(self):
        self.name = ""
        # 门
        self.phylum = ""
        # 纲
        self.classes = ""
        # 目
        self.order = ""
        # 科
        self.family = ""
        # 表面
        self.surface = ""
        # 食物
        self.food = ""
        # 嘴型
        self.mouth = ""
        # 足部
        self.foot = ""
        # 头部
        self.head = ""
        # 纹饰
        self.ornament = ""
        # 牙齿
        self.tooth = ""
        # 会飞: 1; 不会飞: 0;未定义: -1
        self.canfly = -1
        # 生产方式
        self.birth = ""

    def clone(self, _animal):
        self.name = _animal.name
        self.phylum = _animal.phylum
        self.classes = _animal.classes
        self.order = _animal.order
        self.family = _animal.family
        self.surface = _animal.surface
        self.food = _animal.food
        self.mouth = _animal.mouth
        self.foot = _animal.foot
        self.head = _animal.head
        self.ornament = _animal.ornament
        self.tooth = _animal.tooth
        self.canfly = _animal.canfly
        self.birth = _animal.birth

    def output(self):
        print('\n')
        print('该动物', end='')
        if self.birth != "":
            print(self.birth, end='')
            print(',', end='')

        if self.head != "":
            print(self.head, end='')
            print(',', end='')
        if self.mouth != "":
            print(self.mouth, end='')
        if self.tooth != "":
            print(self.tooth, end='')
            print(',', end='')
        if self.food != "":
            print(self.food, end='')
            print(',', end='')
        if self.surface != "":
            print(self.surface, end='')
            print(',', end='')
        if self.ornament != "":
            print(self.ornament, end='')
            print(',', end='')
        if self.foot != "":
            print(self.foot, end='')
            print(',', end='')
        if self.canfly == 1:
            print('会飞, ', end='')
        elif self.canfly == 0:
            print('不会飞, ', end='')
        print('应该属于', end='')
        if self.phylum != "":
            print(self.phylum, end='')
        if self.classes != "":
            print(self.classes, end='')
        if self.order != "":
            print(self.order, end='')
        if self.family != "":
            print(self.family, end='')

            
        if self.name != "":
            print(self.name, end='')
        print('. \n')
