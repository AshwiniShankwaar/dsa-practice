from utils.LinkedList import ListNode as Node


class Solution:
    def __init__(self):
        pass

    def _run(self,list1: Node | None, list2: Node | None):
         head = Node()
         temp = head

         while list1 and list2:
            if list1.val < list2.val:
                temp.next = list1
                list1 = list1.next
            else:
                temp.next = list2
                list2 = list2.next
            temp = temp.next
         while list1:
                temp.next = list1
                temp = temp.next
                list1 = list1.next
         while list2:
                temp.next = list2
                temp = temp.next
                list2 = list2.next
         return head.next
