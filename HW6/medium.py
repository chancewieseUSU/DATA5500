'''
Time complexity: O(n). The function iterates through each item in the array,
comparing each item to find the max and if a new max is found, it sets the last max
to the second_max, and the new item to the new max. Only al
'''


import time

def secondLargest(array):   #creates function with array as input
    max = 0     #initial value
    second_max = 0      #initial value
    for i in array:
        if i > max:             #if i is more than the max, set the second max to the previous max number, and set the new max to i value
            second_max = max
            max = i     
        elif i > second_max and i != max:       #i is greater than second max and not the max, set it to new second max
            second_max = i
    return second_max




start = time.time()     #tracks time

array = [87, 12, 55, 33, 78, 6, 92, 41, 20, 64, 90]     #sets array
print("Second largest in array:", secondLargest(array))   #calls function and prints second max

end = time.time()       #tracks time
print("Time elapsed:",end-start)    #outputs time