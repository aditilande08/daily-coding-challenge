"""
LeetCode #20: Valid Parentheses
Platform: LeetCode
Difficulty: Easy
URL: https://leetcode.com/problems/valid-parentheses/

Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.
Time Complexity: O(n)
Space Complexity: O(n)
"""

class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        matching = {')': '(', '}': '{', ']': '['}
        for char in s:
            if char in matching:
                top = stack.pop() if stack else '#'
                if matching[char] != top:
                    return False
            else:
                stack.append(char)
        return len(stack) == 0

if __name__ == "__main__":
    sol = Solution()
    print(sol.isValid("()[]{}"))  # True
    print(sol.isValid("(]"))      # False
