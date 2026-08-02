<!-- question:1:start -->
## 1. Two Sum
[Link](https://leetcode.com/problems/two-sum)

### Approach
The solution uses a hash table (dictionary) to achieve O(n) time complexity. As we iterate through the array, we maintain a mapping of values to their indices. For each element `nums[i]`, we calculate its complement `c = target - nums[i]`. If the complement exists in our dictionary, we've found our pair and return the stored index of the complement along with the current index. If not, we add the current element and its index to the dictionary for future lookups. This approach efficiently finds the solution in a single pass through the array.

### Complexity
Time: O(n), Space: O(n) - we store at most n elements in the hash table, and we visit each element exactly once.
<!-- question:1:end -->
