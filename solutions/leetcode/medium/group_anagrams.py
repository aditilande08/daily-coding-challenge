"""
LeetCode #49: Group Anagrams
Platform: LeetCode
Difficulty: Medium
URL: https://leetcode.com/problems/group-anagrams/

Given an array of strings strs, group the anagrams together. You can return the answer in any order.

Time Complexity: O(n * k) where n is len(strs) and k is max len of a string
Space Complexity: O(n * k)
"""

from typing import List
from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        ans = defaultdict(list)
        for s in strs:
            count = [0] * 26
            for c in s:
                count[ord(c) - ord('a')] += 1
            ans[tuple(count)].append(s)
        return list(ans.values())

if __name__ == "__main__":
    sol = Solution()
    print(sol.groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
    # Output: [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
