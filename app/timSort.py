MIN_MERGE = 32
 
def calcMinRun(n):
    # Cal the if num is within min merge, set at 32 cause at around 32 it starts to be more effection to use insertion sort. 
    r = 0
    while n >= MIN_MERGE:
        r |= n & 1
        n >>= 1
    return n + r
 
 
#Sort from left to right
def insertionSort(arr, left, right ,sortedList):
    for i in range(left + 1, right + 1):
        j = i
        while j > left and arr[j] < arr[j - 1]:
            arr[j], arr[j - 1] = arr[j - 1], arr[j]
            sortedList[j],sortedList[j-1] = sortedList[j - 1], sortedList[j]
            j -= 1
 
 
# Merge "sort"
def merge(arr, l, m, r,sortedList):
     
    # Break array into 2 part
    # Compare left and right array
    # Since we are sorting the sortedList by arr , we will use temp to arrange our data.
    len1, len2 = m - l + 1, r - m
    left, right = [], []
    leftTemp , rightTemp = [],[]
    for i in range(0, len1):
        left.append(arr[l + i])
        leftTemp.append(sortedList[l + i])
    for i in range(0, len2):
        right.append(arr[m + 1 + i])
        rightTemp.append(sortedList[m + 1 + i])
 
    i, j, k = 0, 0, l
     
    # After comparing, we merge those two array
    # in larger sub array
    while i < len1 and j < len2:
        if left[i] <= right[j]:
            arr[k] = left[i]
            sortedList[k] = leftTemp[i]
            i += 1
 
        else:
            arr[k] = right[j]
            sortedList[k] = rightTemp[j]
            j += 1
 
        k += 1
 
    # Copy remaining elements of left, if any
    while i < len1:
        arr[k] = left[i]
        sortedList[k] = leftTemp[i]
        k += 1
        i += 1
 
    # Copy remaining element of right, if any
    while j < len2:
        arr[k] = right[j]
        sortedList[k] = rightTemp[j]
        k += 1
        j += 1
 
 

def timSort(arr , sortedList):
    n = len(arr)
    minRun = calcMinRun(n)
     
    # Sort individual subarrays of size RUN
    for start in range(0, n, minRun):
        end = min(start + minRun - 1, n - 1)
        insertionSort(arr, start, end, sortedList)

    # Start merging from size RUN (or 32). It will merge
    # to form size 64, then 128, 256 and so on ....
    size = minRun
    while size < n:
         
        # Pick starting point of left sub array. We
        # are going to merge arr[left..left+size-1]
        # and arr[left+size, left+2*size-1]
        # After every merge, we increase left by 2*size
        for left in range(0, n, 2 * size):
 
            # Find ending point of left sub array
            # mid+1 is starting point of right sub array
            mid = min(n - 1, left + size - 1)
            right = min((left + 2 * size - 1), (n - 1))
 
            # Merge sub array arr[left.....mid] &
            # arr[mid+1....right]
            if mid < right:
                merge(arr, left, mid, right,sortedList)

        size = 2 * size
        
    # Rubbish collecting 
    del arr