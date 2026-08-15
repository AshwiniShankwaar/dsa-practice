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
        # if x < 0:
        #     return False
        # if x < 10:
        #     return True
        # reverse_x = 0
        # while True:   #1204321
        #     r = x%10 #4
        #     x = x//10 #120
        #     if x < ((reverse_x*10) + r): #f f f t
        #         break
        #     if x == ((reverse_x*10) + r): #f f f
        #         reverse_x = (reverse_x * 10) + r
        #         break
        #     reverse_x = (reverse_x * 10) + r  # 123
        # if reverse_x != x:
        #     return False
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