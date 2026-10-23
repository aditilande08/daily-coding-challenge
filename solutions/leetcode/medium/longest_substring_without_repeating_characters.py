"""
LeetCode #3: Longest Substring Without Repeating Characters
Platform: LeetCode
Difficulty: Medium
URL: https://leetcode.com/problems/longest-substring-without-repeating-characters/

Given a string s, find the length of the longest substring without repeating characters.

Time Complexity: O(n)
Space Complexity: O(min(m, n)) where m is size of charset
"""

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        char_map = {}
        left = 0
        max_len = 0
        
        for right, char in enumerate(s):
            if char in char_map and char_map[char] >= left:
                left = char_map[char] + 1
            char_map[char] = right
            max_len = max(max_len, right - left + 1)
            
        return max_len

if __name__ == "__main__":
    sol = Solution()
    print(sol.lengthOfLongestSubstring("abcabcbb"))  # 3 ("abc")
    print(sol.lengthOfLongestSubstring("bbbbb"))     # 1 ("b")
    print(sol.lengthOfLongestSubstring("pwwkew"))    # 3 ("wke")
