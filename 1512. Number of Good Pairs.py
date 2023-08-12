class Solution(object):
    def numIdenticalPairs(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        count=0
        for i in range(0,len(nums)-1):#0,1,2,3
            for j in range(i+1,len(nums)):#1,2,3
                if nums[i]==nums[j] and i<j:
                    count+=1
        return count


"""
nums=[]
(i,j)i<j
(1,2) (2,3) (1,1) (1,3)
(1,1)(1,1)(1,1)(1,1)
"""
