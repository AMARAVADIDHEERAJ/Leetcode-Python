class Solution(object):
    def topKFrequent(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """
        a=list(set(nums))
        res=[]
        counts=[]
        for i in a:
            counts.append([nums.count(i),i])
            counts.sort()
        for i in range(-1,-k-1,-1):
            res.append(counts[i][1])
        return res
        
