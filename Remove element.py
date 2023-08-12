class Solution(object):
    def removeElement(self, nums, val):
        """
        :type nums: List[int]
        :type val: int
        :rtype: int
        """
        l=len(nums)
        count=0
        for i in range(l-1,-1,-1):
            if val==nums[i]:
                nums.pop(i)
        print(len(nums))


#0,1,2,3,...
