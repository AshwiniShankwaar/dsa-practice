from typing import List


class Solution:
    def __init__(self):
        pass

    def _run(self, nums: List[int], target: int):
        nums_dict = {}
        for i in range(len(nums)):
            c = target-nums[i]
            if c in nums_dict:
                return [nums_dict[c],i]
            nums_dict[nums[i]] = i