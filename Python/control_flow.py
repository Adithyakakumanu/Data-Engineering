#loops:if-else,if-elif-else,while,do-while,for loop,break,pass,continue


#running sum of 1d array(no:1480)
class Solution:
    def runningSum(nums): #[1,2,3,4]
        sum=0
        a=[]
        for i in range(len(nums)):
            sum=sum+nums[i]
            a.append(sum)
        return a #[1,3,6,10]

#Best time to buy and sell stocks(no:121)
class Solution:
    def maxProfit(self, prices):
        low=high=prices[0]
        maxi=0
        for i in prices[1:]:
            if low>i:
                low=i
                high=0
            if high<i:
                high=i
                maxi=max(high-low,maxi)
        return maxi

#Move Zeros(283)
class Solution(object):
    def moveZeroes(self, nums):
        j=0
        for i in range(len(nums)):
            if nums[i]!=0:
                nums[i],nums[j]=nums[j],nums[i]
                j=j+1