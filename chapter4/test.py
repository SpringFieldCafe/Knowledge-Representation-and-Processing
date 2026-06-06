import expertsys
from animal import animal

if __name__ == '__main__':
    aniexpert = expertsys.expertsys()

    ani1 = animal()
    ani1.birth = '卵生'
    ani1.canfly = 1
    ani1.head = '红顶'
    ani1.foot = '细腿'

    ani2 = animal()
    ani2.birth = '胎生'
    ani2.food = '肉'
    ani2.ornament = '褐色斑纹'

    aniexpert.setFacts([ani1, ani2])
    aniexpert.forwardReasoning()