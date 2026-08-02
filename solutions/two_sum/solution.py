from typing import List


class Solution:
    def __init__(self):
        pass

    def _run(self, nums: List[int], target: int):
        # sort indices by value so the two-pointer scan works but we can
        # still return the ORIGINAL indices (sorting nums directly loses them)
        # order = sorted(range(len(nums)), key=lambda k: nums[k])
        # i = 0
        # j = len(nums) - 1  # last valid index, not len(nums)
        # while i < j:
        #     total = nums[order[i]] + nums[order[j]]  # 'sum' shadows the builtin
        #     if total == target:
        #         return sorted([order[i], order[j]])
        #     elif total > target:
        #         j -= 1  # 'j = - 1' assigned -1 instead of decrementing
        #     else:
        #         i += 1  # same bug: 'i = + 1' assigned +1
        # return []
        nums_dict = {}
        for i in range(len(nums)):
            c = target-nums[i]
            if c in nums_dict:
                return [nums_dict[c],i]
            nums_dict[nums[i]] = i