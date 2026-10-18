"""
LeetCode #53: Maximum Subarray
Platform: LeetCode
Difficulty: Medium
URL: https://leetcode.com/problems/maximum-subarray/

Given an integer array nums, find the subarray with the largest sum, and return its sum. (Kadane's Algorithm)
Time Complexity: O(n)
Space Complexity: O(1)
"""

from typing import List

class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        max_so_far = nums[0]
        curr_max = nums[0]
        for num in nums[1:]:
            curr_max = max(num, curr_max + num)
            max_so_far = max(max_so_far, curr_max)
        return max_so_far

if __name__ == "__main__":
    sol = Solution()
    print(sol.maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))  # Output: 6
