from typing import List
class Solution:
    def __init__(self):
        pass

    def _run(self,strs: List[str]):
        longest_prefix = strs[0]

        for i in range(1,len(strs)):
            while not strs[i].startswith(longest_prefix):
               longest_prefix = longest_prefix[:-1]
        return longest_prefix
