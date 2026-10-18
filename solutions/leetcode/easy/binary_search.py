"""
LeetCode #704: Binary Search
Platform: LeetCode
Difficulty: Easy
URL: https://leetcode.com/problems/binary-search/

Given an array of integers nums which is sorted in ascending order, and an integer target, write a function to search target in nums.
Time Complexity: O(log n)
Space Complexity: O(1)
"""

from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        low, high = 0, len(nums) - 1
        while low <= high:
            mid = (low + high) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        return -1

if __name__ == "__main__":
    sol = Solution()
    print(sol.search([-1, 0, 3, 5, 9, 12], 9))  # Output: 4
