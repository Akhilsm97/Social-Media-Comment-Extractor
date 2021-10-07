# from stemming.porter2 import stem
# 
# def steming(commend):
#         stemmed=""
#         splited=commend.split()
#         print splited
#         for i in splited:
#                 stemmed=stemmed+" "+stem(i)
#         print stemmed
#         return stemmed
#-------------------------------------------------------------------------------
# from nltk.stem.lancaster import LancasterStemmer
# st=LancasterStemmer()
# def steming(commend):
#         stemmed=""
#         splited=commend.split()
#         print splited
#         for i in splited:
#                 stemmed=stemmed+" "+st.stem(i)
#         print stemmed
#-------------------------------------------------------------------------------
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
def steming(commend):
        stemmed=""
        splited=commend.split()
        print(splited)
        for i in splited:
                stemmed=stemmed+" "+lemmatizer.lemmatize(i, pos='v')
        print(stemmed)
        return stemmed


