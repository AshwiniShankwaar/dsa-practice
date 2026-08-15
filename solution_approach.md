<!-- question:1:start -->
## 1. Two Sum
[Link](https://leetcode.com/problems/two-sum)

### Approach
The solution uses a hash table (dictionary) to achieve O(n) time complexity. As we iterate through the array, we maintain a mapping of values to their indices. For each element `nums[i]`, we calculate its complement `c = target - nums[i]`. If the complement exists in our dictionary, we've found our pair and return the stored index of the complement along with the current index. If not, we add the current element and its index to the dictionary for future lookups. This approach efficiently finds the solution in a single pass through the array.

### Complexity
Time: O(n), Space: O(n) - we store at most n elements in the hash table, and we visit each element exactly once.
<!-- question:1:end -->

<!-- question:9:start -->
## 9. Palindrome Number
[Link](https://leetcode.com/problems/palindrome-number)

### Approach
The solution reverses only half of the number and compares it with the remaining half. 

The algorithm works by:
1. Handling edge cases: negative numbers, single digits, and numbers ending in 0 (except 0 itself)
2. Building `reverse_x` by taking digits from the end of `x` and prepending them
3. Simultaneously dividing `x` by 10 to remove the processed digit
4. Stopping when `x <= reverse_x`, which means we've processed half the digits
5. Checking if the remaining `x` equals `reverse_x` (odd digit count) or `reverse_x//10` (even digit count)

This approach avoids converting to a string and only reverses half the number, making it efficient.

### Complexity
Time: O(log10(n)), Space: O(1) - the algorithm processes each digit once by repeatedly dividing by 10, using only constant extra space.
<!-- question:9:end -->
