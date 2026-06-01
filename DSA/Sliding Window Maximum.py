from collections import deque

'''def sliding_max(arr, k):
    d = deque()
    result= []
    for i in range(len(arr)):
        if d:
            if(arr[i]>d[-1]):
                d.append(arr[i])
            else:
                d.appendleft(arr[i])
        else:
            d.append(arr[i])
        if(i>=k-1):
            result.append(d[-1])
    print(result)'''

from collections import deque

def sliding_max(arr, k):
    d = deque()  # stores indices, not values
    result = []
    for i in range(len(arr)):
        # remove index if outside window
        if d and d[0] < i - k + 1:
            d.popleft()
        # remove smaller elements from back
        while d and arr[d[-1]] < arr[i]:
            d.pop()
        d.append(i)
        # record max when window is complete
        if i >= k - 1:
            result.append(arr[d[0]])
    print(result)

        
sliding_max([1,3,-1,-3,5,3,6,7], 3)  # [3,3,5,5,6,7]
sliding_max([1,2,3,4,5], 2)           # [2,3,4,5]
sliding_max([5], 1)                    # [5]
sliding_max([5,4,3,2,1], 3)  # should be [5,5,5]