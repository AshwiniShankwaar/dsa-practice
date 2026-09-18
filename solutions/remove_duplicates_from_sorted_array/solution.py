class Solution:
    def __init__(self):
        pass

    def _run(self,nums: list[int]):
        if not nums:
            return 0
        j = 0
        for i in range(1,len(nums)):
            if nums[i] == nums[j]:
                continue
            else:
                j +=1
                nums[j] = nums[i]
        return j+1