#length of last word(no:58)
class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        words = s.strip().split()
        
        if not words:
            return 0
        
        return len(words[-1])
#Reverse String(344)
class Solution:
    def reverseString(self, s):
        left = 0
        right = len(s) - 1
        while left < right:
            s[left], s[right] = s[right], s[left]
            left += 1
            right -= 1
#Valid Anagram(242)
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        for i in set(s):
            if s.count(i) != t.count(i):
                return False
        return True
#Valid Palindrome(125)
class Solution:
    def isPalindrome(self, s: str) -> bool:
        new = ""
        for i in s:
            if i.isalnum():
                new += i.lower()
        return new == new[::-1]
        
#Maximum Subarray(53)

class Solution:
    def maxSubArray(self, nums):
        maxSum = float('-inf')
        currentSum = 0
        
        for num in nums:
            currentSum += num
            
            if currentSum > maxSum:
                maxSum = currentSum
            
            if currentSum < 0:
                currentSum = 0
        
        return maxSum