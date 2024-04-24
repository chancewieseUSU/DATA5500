'''
Time complexity: O(n). The function iterates through each item in the array,
adding each number to a sum. Only performs one altercation in each iteration.
'''


import time

def sumOfArray(array):  #creates function with array as input
    sum = 0     #initial value
    for i in array: #add new i to sum
        sum += i
    return sum
    



start = time.time()     #tracks time

array = [1,2,3,4,5]     #sets array
print("Sum of array:", sumOfArray(array)) #calls function and prints sum

end = time.time()       #tracks time
print("Time elapsed:",end-start)    #outputs time