'''
Time complexity: O(n). The function iterates through each item in the array,
comparing the iterations to find maximum and minimum, and subtracting that 
to find the greatest difference. Only iterates through the array once.
'''


import time

def maxDifference(array):   #creates function with array as input
    max = 0     #initial value
    min = 101   #initial value
    for i in array:     
        if i > max:     #if i is greater than the max then new max is i
            max = i
        elif i < min:   #if i is less than max and min then it is new min
            min = i
    return max-min      #outputs max-min


start = time.time()     #tracks time

array = [87, 12, 55, 33, 78, 6, 92, 4, 41, 20, 64, 90]      #sets array
print("Biggest Difference:", maxDifference(array))   #calls function and prints difference

end = time.time()       #tracks time
print("Time elapsed:",end-start)    #outputs time