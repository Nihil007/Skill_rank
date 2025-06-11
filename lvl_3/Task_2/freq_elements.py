# import build in function to count
from collections import Counter

def mostfrequent(nums,k):

    # count frequency of each number 
    freq = Counter(nums)

    # get common elements as per k
    common = freq.most_common(k) 

    # extract elements
    result = [item for item,count in common]

    # return frequent element
    return result


