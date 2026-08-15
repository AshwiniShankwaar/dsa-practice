class Solution:
    def __init__(self):
        pass

    def _run(self,x: int):
        # Brute force approach
        # if x < 0:
        #     return False
        # digits = []
        # while x>0:
        #     r = round(x%10)
        #     x = x//10
        #     digits.append(r)
        # print(digits)
        # i = 0
        # j = len(digits)-1
        # while i<j:
        #     if digits[i]!=digits[j]:
        #         return False
        #     i+=1
        #     j-=1
        # return True
        # Best optimized approach convert the numer in str and reverse using [::-1] and compare.
        if x < 0:
            return False
        if x < 10:
            return True
        if x%10 == 0:
            return False
        reverse_x = 0  #
        while x >reverse_x:  # t
            reverse_x = (reverse_x*10)+(x%10)
            x = x//10 # 100
        if x == reverse_x or x == (reverse_x//10):
            return True
        return False