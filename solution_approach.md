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

<!-- question:13:start -->
## 13. Roman to Integer
[Link](https://leetcode.com/problems/roman-to-integer)

### Approach
The solution processes the Roman numeral string from right to left, which simplifies the subtraction logic. Starting from the last character, each value is looked up in a dictionary mapping Roman symbols to their integer values.

The algorithm maintains a running total. For the last character, it always adds its value since there's no following character to compare against. For all other characters, it compares the current character's value with the next character's value to the right. If the current value is smaller than the next, it subtracts (handling cases like IV, IX, etc.). Otherwise, it adds the current value.

This right-to-left approach naturally handles the subtraction rule because smaller values appearing before larger values in the original string will be processed when we encounter them from the right.

### Complexity
Time: O(n), Space: O(1)
<!-- question:13:end -->

<!-- question:14:start -->
## 14. Longest Common Prefix
[Link](https://leetcode.com/problems/longest-common-prefix)

### Approach
The algorithm starts by assuming the first string is the initial longest common prefix. It then iterates over the remaining strings, and for each string, it repeatedly removes the last character of the prefix until the string starts with the current prefix. This shrink‑and‑verify process continues until all strings have been checked, at which point the remaining prefix is the longest common prefix among all strings.

### Complexity
Time: O(n * m), where n is the number of strings and m is the length of the first string; each character is removed at most once per string. Space: O(1) additional space, as the prefix is modified in place.
<!-- question:14:end -->
