import animal
import rule


class expersys(object):
    def __init__(self):
        self.facts=[]
        self.rules=[]
        self.dataset=[]

        
        self.setRules()
