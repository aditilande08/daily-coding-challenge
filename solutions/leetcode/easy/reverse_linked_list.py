"""
LeetCode #206: Reverse Linked List
Platform: LeetCode
Difficulty: Easy
URL: https://leetcode.com/problems/reverse-linked-list/

Given the head of a singly linked list, reverse the list, and return the reversed list.
Time Complexity: O(n)
Space Complexity: O(1)
"""

from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        curr = head
        while curr:
            next_temp = curr.next
            curr.next = prev
            prev = curr
            curr = next_temp
        return prev

if __name__ == "__main__":
    # Create 1 -> 2 -> 3 -> None
    head = ListNode(1, ListNode(2, ListNode(3)))
    sol = Solution()
    rev = sol.reverseList(head)
    vals = []
    while rev:
        vals.append(rev.val)
        rev = rev.next
    print(vals)  # [3, 2, 1]
