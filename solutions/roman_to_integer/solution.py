class Solution:
    def __init__(self):
        pass

    def _run(self, s: str):
        _dict = {
            "I": 1,
            "V": 5,
            "X": 10,
            "L": 50,
            "C": 100,
            "D": 500,
            "M": 1000
        }
        c = list(s)
        number = 0
        for i in range(len(c)-1,-1,-1):
            x = _dict.get(c[i])
            if i == (len(c)-1):
                number += x
            else:
                y = _dict.get(c[i+1])
                if x < y:
                    number-=x
                else:
                    number+=x
        return number