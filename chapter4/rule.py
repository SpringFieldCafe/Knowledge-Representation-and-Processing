from animal import animal

class rule(object):
    def __init__(self):
        self.antecedent = animal()
        self.consequent = animal()

    def setAntecedent(self, animal):
        self.antecedent.clone(animal)

    def setConsequent(self, animal):
        self.consequent.clone(animal)

    # 规则匹配
    def match(self, animal):
        result = True
        if self.antecedent.canfly != -1:
            if self.antecedent.canfly != animal.canfly:
                result = False
                return result
        if self.antecedent.classes != "":
            if self.antecedent.classes != animal.classes:
                result = False
                return result
        if self.antecedent.family != "":
            if self.antecedent.family != animal.family:
                result = False
                return result
        if self.antecedent.food != "":
            if self.antecedent.food != animal.food:
                result = False
                return result
        if self.antecedent.foot != "":
            if self.antecedent.foot != animal.foot:
                result = False
                return result
        if self.antecedent.head != "":
            if self.antecedent.head != animal.head:
                result = False
                return result
        if self.antecedent.mouth != "":
            if self.antecedent.mouth != animal.mouth:
                result = False
                return result
        if self.antecedent.name != "":
            if self.antecedent.name != animal.name:
                result = False
                return result
        if self.antecedent.order != "":
            if self.antecedent.order != animal.order:
                result = False
                return result
        if self.antecedent.ornament != "":
            if self.antecedent.ornament != animal.ornament:
                result = False
                return result
        if self.antecedent.surface != "":
            if self.antecedent.surface != animal.surface:
                result = False
                return result
        if self.antecedent.tooth != "":
            if self.antecedent.tooth != animal.tooth:
                result = False
                return result
        if self.antecedent.birth != "":
            if self.antecedent.birth != animal.birth:
                result = False
                return result
        if self.antecedent.phylum != "":
            if self.antecedent.phylum != animal.phylum:
                result = False
                return result
        return result

    # 规则执行
    def execute(self, animal):
        if self.consequent.canfly != -1:
            animal.canfly = self.consequent.canfly
        if self.consequent.classes != "":
            animal.classes = self.consequent.classes
        if self.consequent.family != "":
            animal.family = self.consequent.family
        if self.consequent.food != "":
            animal.food = self.consequent.food
        if self.consequent.foot != "":
            animal.foot = self.consequent.foot
        if self.consequent.head != "":
            animal.head = self.consequent.head
        if self.consequent.mouth != "":
            animal.mouth = self.consequent.mouth
        if self.consequent.name != "":
            animal.name = self.consequent.name
        if self.consequent.order != "":
            animal.order = self.consequent.order
        if self.consequent.ornament != "":
            animal.ornament = self.consequent.ornament
        if self.consequent.surface != "":
            animal.surface = self.consequent.surface
        if self.consequent.tooth != "":
            animal.tooth = self.consequent.tooth
        if self.consequent.birth != "":
            animal.birth = self.consequent.birth
        if self.consequent.phylum != "":
            animal.phylum = self.consequent.phylum