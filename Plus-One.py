class Solution(object):
    def plusOne(self, digits):
        """
        :type digits: List[int]
        :rtype: List[int]
        """
        n=len(digits)
        s=0
        for i in digits:
            s=s*10+i
        s=s+1
        ls=[]
        for i in str(s):
            ls.append(int(i))
        return ls
"""
1,2,3
123+1
1,2,4

"""
