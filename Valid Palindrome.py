class Solution(object):
    def isPalindrome(self, s):
        y=s.lower()
        x=''.join(letter for letter in y if letter.isalnum())
        rev=x[::-1]
        if(rev==x):
            return True
        else:
            return False
