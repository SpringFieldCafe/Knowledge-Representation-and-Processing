import nltk

lp=nltk.sem.logic.LogicParser()
P=lp.parse('man(Socrates)')
Q=lp.parse('all x (man(x)->mortal(x))')
R=lp.parse('mortal(Socrates)')

prover1=nltk.inference.prover9.Prover9()
print(prover1.prove(R,[P,Q]))

# from nltk.sem import Expression
# from nltk.inference import Prover9
# read=Expression.fromstring
# p1=read('man(socrates)')
# p2=read('all x.(man(x) -> mortal(x))');
# c=read('mortal(socrates)')
# print(Prover9().prove(c,[p1,p2]))