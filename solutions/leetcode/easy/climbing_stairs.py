"""
LeetCode #70: Climbing Stairs
Platform: LeetCode
Difficulty: Easy
URL: https://leetcode.com/problems/climbing-stairs/

You are climbing a staircase. It takes n steps to reach the top.
Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

Time Complexity: O(n)
Space Complexity: O(1)
"""

class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n
        prev, curr = 1, 2
        for _ in range(3, n + 1):
            prev, curr = curr, prev + curr
        return curr

if __name__ == "__main__":
    sol = Solution()
    print(sol.climbStairs(2))  # 2
    print(sol.climbStairs(3))  # 3
    print(sol.climbStairs(5))  # 8
