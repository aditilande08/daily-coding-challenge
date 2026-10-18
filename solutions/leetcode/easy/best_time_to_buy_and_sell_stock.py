"""
LeetCode #121: Best Time to Buy and Sell Stock
Platform: LeetCode
Difficulty: Easy
URL: https://leetcode.com/problems/best-time-to-buy-and-sell-stock/

You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.
Time Complexity: O(n)
Space Complexity: O(1)
"""

from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        min_price = float('inf')
        max_profit = 0
        for p in prices:
            if p < min_price:
                min_price = p
            elif p - min_price > max_profit:
                max_profit = p - min_price
        return max_profit

if __name__ == "__main__":
    s = Solution()
    print(s.maxProfit([7, 1, 5, 3, 6, 4]))  # Output: 5
