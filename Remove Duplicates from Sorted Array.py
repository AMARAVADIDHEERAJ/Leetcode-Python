class Solution(object):
    def removeDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        l=len(nums)
        unique=[]
        for i in nums:
            if i in unique:
                continue
            else:
                unique.append(i)
        for i in range(len(unique)):
            nums[i]=unique[i]
        return len(unique)


"""
first oka loop and inko list tho 
aa array lo unna unique elements emunnayo copy chesko 
then unique elements in array length ni return chey and before that 
copy unique elements (lets say m elements are unique)
copy those elements into first m places of nums array in order saying nums[i] = unique[i]

"""        
