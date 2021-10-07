from nltk import ngrams

def one_gram(commend):
    gramlist=[]
    gram = ngrams(commend.split(), 1)
    for i in gram:
        gramlist.append(i)
    return gramlist
def two_gram(commend):
    gramlist=[]
    gram = ngrams(commend.split(), 2)
    for i in gram:
        gramlist.append(i)
    return gramlist
def three_gram(commend):
    gramlist=[]
    gram = ngrams(commend.split(), 3)
    for i in gram:
        gramlist.append(i)
    return gramlist
def four_gram(commend):
    gramlist=[]
    gram = ngrams(commend.split(), 4)
    for i in gram:
        gramlist.append(i)
    return gramlist

