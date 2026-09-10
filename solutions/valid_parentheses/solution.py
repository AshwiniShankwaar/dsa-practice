class Solution:
    def __init__(self):
        pass

    def _run(self,s: str):
        stack = []
        map = {
            ")":"(",
            "}":"{",
            "]":"["
        }
        for c in s:
            if c in map:
                if stack:
                    x = stack.pop()
                else:
                    x = "#"
                if x != map[c]:
                    return False
            else:
                stack.append(c)
        return len(stack) == 0