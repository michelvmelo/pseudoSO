from operator import itemgetter
from itertools import groupby

data = [2, 2, 4, 5, 3, 3, 3, 15, 16, 17]
cont = 0
for k, g in groupby(enumerate(data), itemgetter(1)):
    #for x in g:
    #    print " X %s e k %s." %(g, k)
    #print(k) #chave
    cont +=1
    
    print(cont)
    print map(itemgetter(1), g)
