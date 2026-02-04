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
def migratoryBirds(arr):
    # Write your code here
    d={}
    for i in range(len(arr)):
        if arr[i] in d:
            d[arr[i]]=d[arr[i]]+1
        else:
            d[arr[i]]=1
    max_count = max(d.values())
    min_bird = float('inf')

    for bird, count in d.items():
        if count == max_count and bird < min_bird:
            min_bird = bird
    return min_bird

def diagonalDifference(arr):
    n = len(arr)
    primary_sum = 0
    secondary_sum = 0
    for i in range(n):
        primary_sum += arr[i][i]      
        secondary_sum += arr[i][n - i - 1] 
    return abs(primary_sum - secondary_sum)

def gradingStudents(grades):
    for i in range(len(grades)):
        if grades[i]<38:
            grades[i]=grades[i]
        elif (((grades[i]//5)+1)*5)-grades[i] >=3:
            grades[i]=grades[i]
        else:
            grades[i]=((grades[i]//5)+1)*5
    return grades

def timeConversion(s):
    if s[-2:] == "PM":
        hh = int(s[:2])
        if hh != 12:
            hh += 12
        return str(hh) + s[2:-2]
    else:  # AM
        if s[:2] == "12":
            return "00" + s[2:-2]
        return s[:-2]
def caesarCipher(s, k):
    k = k % 26
    result = ""

    for ch in s:
        if 'a' <= ch <= 'z':
            result += chr((ord(ch) - ord('a') + k) % 26 + ord('a'))
        elif 'A' <= ch <= 'Z':
            result += chr((ord(ch) - ord('A') + k) % 26 + ord('A'))
        else:
            result += ch

    return result

def dayOfProgrammer(year):
    if year == 1918:
        return "26.09.1918"

    # Julian calendar
    if year < 1918:
        leap = (year % 4 == 0)
    # Gregorian calendar
    else:
        leap = (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0)

    if leap:
        return f"12.09.{year}"
    else:
        return f"13.09.{year}"
