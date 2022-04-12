import random
from unittest import result

#make two arrays

#find a number that exists within both arrays
#list1 = [random.randint(1, 100) for i in range(1,101)]
#list2 = [random.randint(1, 100) for i in range(1,101)]
list1 = [1, 2, 3, 4, 5]
list2 = [1, 6, 7, 8, 5]


def getCommonNumber(list1, list2, result):
    result = 0
    for x in list1:
        if x in list2:
            result = result + 1
            
            

    
    print (result)
 
    

getCommonNumber(list1, list2, result)



        







