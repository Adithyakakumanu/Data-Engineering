def sockMerchant(n, ar):
    d={}
    s=0
    for i in range(n):
        if ar[i] in d:
            d[ar[i]]=d[ar[i]]+1
        else:
            d[ar[i]]=1
        if d[ar[i]]%2==0:
            s=s+1
    return s

def breakingRecords(scores):
    min=max=scores[0]
    c1=c2=0
    for i in range(len(scores)):
        if scores[i]<min:
            min=scores[i]
            c2=c2+1
        elif scores[i]>max:
            max=scores[i]
            c1=c1+1
    return c1,c2

def quickSort(arr):
    pivot = arr[0]
    left = []
    right = []
    equal = []

    for x in arr:
        if x < pivot:
            left.append(x)
        elif x > pivot:
            right.append(x)
        else:
            equal.append(x)

    return left + equal + right

def superReducedString(s):
    i = 0
    while i < len(s) - 1:
        if s[i] == s[i + 1]:
            s = s[:i] + s[i + 2:]
            i = max(i - 1, 0)
        else:
            i += 1
    return s if s else "Empty String"
