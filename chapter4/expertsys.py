from animal import animal
from rule import rule


class expertsys(object):
    def __init__(self):
        self.facts=[]
        self.rules=[]
        self.dataset=[]


        self.setRules()

    # 建立规则库
    def setRules(self):
        R1 = rule()
        # 设置前件
        R1_antecedent = animal()
        R1_antecedent.birth = '胎生'
        R1.setAntecedent(R1_antecedent)
        # 设置后件
        R1_consequent = animal()
        R1_consequent.classes = '哺乳纲'
        R1.setConsequent(R1_consequent)
        self.rules.append(R1)

        R2 = rule()
        # 设置前件
        R2_antecedent = animal()
        R2_antecedent.birth = '卵生'
        R2_antecedent.canfly = 1
        R2.setAntecedent(R2_antecedent)
        # 设置后件
        R2_consequent = animal()
        R2_consequent.classes = '鸟纲'
        R2.setConsequent(R2_consequent)
        self.rules.append(R2)

        R3 = rule()
        # 设置前件
        R3_antecedent = animal()
        R3_antecedent.surface = '毛发'
        R3.setAntecedent(R3_antecedent)
        # 设置后件
        R3_consequent = animal()
        R3_consequent.classes = '哺乳纲'
        R3.setConsequent(R3_consequent)
        self.rules.append(R3)

        R4 = rule()
        # 设置前件
        R4_antecedent = animal()
        R4_antecedent.birth = '羽毛'
        R4.setAntecedent(R4_antecedent)
        # 设置后件
        R4_consequent = animal()
        R4_consequent.classes = '鸟纲'
        R4.setConsequent(R4_consequent)
        self.rules.append(R4)

        R5 = rule()
        # 设置前件
        R5_antecedent = animal()
        R5_antecedent.mouth = '喙'
        R5.setAntecedent(R5_antecedent)
        # 设置后件
        R5_consequent = animal()
        R5_consequent.classes = '鸟纲'
        R5.setConsequent(R5_consequent)
        self.rules.append(R5)

        R6 = rule()
        # 设置前件
        R6_antecedent = animal()
        R6_antecedent.food = '肉'
        R6.setAntecedent(R6_antecedent)
        # 设置后件
        R6_consequent = animal()
        R6_consequent.order = '食肉目'
        R6.setConsequent(R6_consequent)
        self.rules.append(R6)

        R7 = rule()
        # 设置前件
        R7_antecedent = animal()
        R7_antecedent.food = '草'
        R7.setAntecedent(R7_antecedent)
        # 设置后件
        R7_consequent = animal()
        R7_consequent.order = '食草目'
        R7.setConsequent(R7_consequent)
        self.rules.append(R7)

        R8 = rule()
        # 设置前件
        R8_antecedent = animal()
        R8_antecedent.foot = '爪'
        R8.setAntecedent(R8_antecedent)
        # 设置后件
        R8_consequent = animal()
        R8_consequent.phylum = '有爪门'
        R8.setConsequent(R8_consequent)
        self.rules.append(R8)

        R9 = rule()
        # 设置前件
        R9_antecedent = animal()
        R9_antecedent.foot = '蹄'
        R9_antecedent.classes = '哺乳纲'
        R9.setAntecedent(R9_antecedent)
        # 设置后件
        R9_consequent = animal()
        R9_consequent.order = '有蹄目'
        R9.setConsequent(R9_consequent)
        self.rules.append(R9)

        R10 = rule()
        # 设置前件
        R10_antecedent = animal()
        R10_antecedent.phylum = '有爪门'
        R10_antecedent.tooth = '有犬齿'
        R10.setAntecedent(R10_antecedent)
        # 设置后件
        R10_consequent = animal()
        R10_consequent.order = '食肉目'
        R10.setConsequent(R10_consequent)
        self.rules.append(R10)

        R11 = rule()
        # 设置前件
        R11_antecedent = animal()
        R11_antecedent.phylum = '有爪门'
        R11_antecedent.order = '食肉目'
        R11_antecedent.classes = '鸟纲'
        R11_antecedent.canfly = 1
        R11.setAntecedent(R11_antecedent)
        # 设置后件
        R11_consequent = animal()
        R11_consequent.family = '鹰'
        R11.setConsequent(R11_consequent)
        self.rules.append(R11)

        R12 = rule()
        # 设置前件
        R12_antecedent = animal()
        R12_antecedent.order = '食肉目'
        R12_antecedent.classes = '哺乳纲'
        R12_antecedent.ornament = '褐色斑纹'
        R12.setAntecedent(R12_antecedent)
        # 设置后件
        R12_consequent = animal()
        R12_consequent.family = '猫'
        R12.setConsequent(R12_consequent)
        self.rules.append(R12)

        R13 = rule()
        # 设置前件
        R13_antecedent = animal()
        R13_antecedent.order = '有蹄目'
        R13_antecedent.ornament = '黑白斑纹'
        R13.setAntecedent(R13_antecedent)
        # 设置后件
        R13_consequent = animal()
        R13_consequent.family = '斑马'
        R13.setConsequent(R13_consequent)
        self.rules.append(R13)

        R14 = rule()
        # 设置前件
        R14_antecedent = animal()
        R14_antecedent.order = '食肉目'
        R14_antecedent.classes = '哺乳纲'
        R14_antecedent.ornament = '王字纹'
        R14.setAntecedent(R14_antecedent)
        # 设置后件
        R14_consequent = animal()
        R14_consequent.family = '虎'
        R14.setConsequent(R14_consequent)
        self.rules.append(R14)

        R15 = rule()
        # 设置前件
        R15_antecedent = animal()
        R15_antecedent.foot = '细腿'
        R15_antecedent.head = '红顶'
        R15_antecedent.classes = '鸟纲'
        R15.setAntecedent(R15_antecedent)
        # 设置后件
        R15_consequent = animal()
        R15_consequent.family = '丹顶鹤'
        R15.setConsequent(R15_consequent)
        self.rules.append(R15)



    def setFacts(self,_facts):
        for ani in _facts:
            f=animal()
            f.clone(ani)
            self.facts.append(f)
            d=animal()
            d.clone(ani)
            self.dataset.append(d)

    def forwardReasoning(self):
        for d in self.dataset:
            for r in self.rules:
                if r.match(d):
                    r.execute(d)

            d.output()