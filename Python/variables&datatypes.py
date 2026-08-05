#variables:name refer to a value stored in memory.used to store data it can be reused and manipulated.
a=10
b=15
print("the sum is: ",(a+b))
print(f'the sum of {a} and {b} is {a+b}')
print("the number is %d and %d "%(a,b))
print("the number are {} and {}".format(a,b))

#Data types :The type of data a variable holds and what operations can be performed on it.
# Numerical:int,float,complex.  Boolean:bool  Sequence:str,list,tuple.  Set data type:set mapping:dict.  Type Conversion:int(),float(),str()   Mutable:list:[1,2,3],dict:{"a":1},set:{1,2} Immutable:int:10,float:3.14,str:"Hello",tuple:(1,2)

print(type(10))
age = 22
price = 99.50
name = "Adithya"
is_passed = True
print(f"Name: {name}")
print(f"Age: {age}")
print(f"Passed: {is_passed}")
print(f"Product price: {price}")

#Intersection of Two Arrays
class Solution(object):
    def intersection(self, nums1, nums2):
        a=set(nums1)
        b=set(nums2)
        c=list(a.intersection(b))
        return c