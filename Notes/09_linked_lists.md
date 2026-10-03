# 09 — Linked Lists

## Idea
A linked list is a chain of boxes. Each box holds a `val` and a `next` pointer to the next box.
Repo helper: `utils/LinkedList.py` (`ListNode`, `LinkedListUtils.build` / `to_list`).

## Three tricks
1. **Dummy head**: a fake node in front. It removes special cases for the first node.
   ```python
   def remove_head_if_zero(head):
       dummy = ListNode(0, head)     # fake node in front
       prev, cur = dummy, head
       while cur:
           if cur.val == 0:
               prev.next = cur.next  # unlink, no special case for the head
           else:
               prev = cur
           cur = cur.next
       return dummy.next
   ```
2. **Two pointers**: a fast one (2 steps) and a slow one (1 step). When fast reaches the end, slow is in the middle.
3. **Save before you rewire**: `nxt = cur.next` first, then change `cur.next`.

## Template: reverse a list
```python
def reverse(head):
    prev = None
    cur = head
    while cur:
        nxt = cur.next      # save the rest
        cur.next = prev     # flip the arrow
        prev = cur          # move prev forward
        cur = nxt           # move cur forward
    return prev
```

## Template: cycle detection
If the fast pointer ever meets the slow one, there is a loop.
```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False
```

## Classic problems
Reverse Linked List, Merge Two Sorted Lists (solved in this repo), Linked List Cycle,
Remove Nth Node From End (gap of n between two pointers), Middle of the List,
Add Two Numbers (carry), Palindrome Linked List (find middle, reverse second half).

## Mistakes
- Losing the rest of the list because you changed `next` too early.
- `while fast.next` without checking `fast` first → crash.
- Use `is` to compare nodes, `==` only for values.
