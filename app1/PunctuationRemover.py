def RemovePunctuations(commend):
    punctuations=['.', ',', '"', "'", '?', '$', '!', ':', ';', '(', ')', '>','<','+','=','|','-','[', ']', '{', '}', '@','%','!','^','*','_','/','...','#']
    a=""
    for i in range(0,len(commend)):
        if commend[i] not in punctuations:
            a=a+commend[i]
    print (a)
    return a
