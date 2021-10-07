from itertools import chain
from nltk.corpus import wordnet
text="change"
text1=[]
def synonyms(tok):
  final=tok
  try:
    stemmed=tok
    print(stemmed)
    stmd=[]
    for i in stemmed:
        lemmas=[]
        tl=[]
        synonyms = wordnet.synsets(i)
        lemmas = list(chain.from_iterable([word.lemma_names() for word in synonyms]))
        l=set(lemmas)
        t=list(l)
        for r in t:
            tl.append(r)
        RI=tl
        if len(tl):
            for k in tl:
                if k==i:
                    RI.remove(i)
                else :
                    pass
            for h in RI:
                for a in stemmed:
                    if a==h:
                        stemmed.remove(a)
    
    print (stemmed)
    for i in stemmed:
        if i not in stmd:
            stmd.append(i)
    print (stmd)
    return  stmd
  except:
      return final
