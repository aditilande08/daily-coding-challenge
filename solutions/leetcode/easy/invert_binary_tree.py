"""
LeetCode #226: Invert Binary Tree
Platform: LeetCode
Difficulty: Easy
URL: https://leetcode.com/problems/invert-binary-tree/

Given the root of a binary tree, invert the tree, and return its root.
Time Complexity: O(n)
Space Complexity: O(h) where h is tree height
"""

from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None
        root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
        return root
