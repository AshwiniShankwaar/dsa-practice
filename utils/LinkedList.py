class ListNode:
    """
    Singly Linked List Node
    """
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class DoublyListNode:
    """
    Doubly Linked List Node
    """
    def __init__(self, val=0, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next


class LinkedListUtils:

    @staticmethod
    def build(values, doubly=False):
        """
        Build a singly or doubly linked list.

        Args:
            values: List of values.
            doubly: False -> Singly
                     True  -> Doubly

        Returns:
            Head node.
        """
        if not values:
            return None
        if doubly:
            dummy = DoublyListNode()
        else:
            dummy = ListNode()
        current = dummy
        for value in values:
            if doubly:
                node = DoublyListNode(value)
                node.prev = current if current != dummy else None
            else:
                node = ListNode(value)
            current.next = node
            current = node
        return dummy.next

    @staticmethod
    def to_list(head):
        """
        Convert a linked list to a Python list.
        Works for both singly and doubly linked lists.
        """
        result = []
        while head:
            result.append(head.val)
            head = head.next
        return result

    @staticmethod
    def print(head):
        """
        Print a linked list.
        """
        if head is None:
            print("None")
            return

        print(" -> ".join(map(str, LinkedListUtils.to_list(head))) + " -> None")

    @staticmethod
    def print_reverse(tail):
        """
        Print a doubly linked list in reverse.
        """
        if tail is None:
            print("None")
            return

        values = []
        while tail:
            values.append(str(tail.val))
            tail = tail.prev
        values.append("None")
        print(" <- ".join(values))

    @staticmethod
    def get_tail(head):
        """
        Return the tail of the linked list.
        Useful for reverse traversal in doubly linked lists.
        """
        if head is None:
            return None
        while head.next:
            head = head.next
        return head

    @staticmethod
    def length(head):
        """
        Return the length of the linked list.
        """
        count = 0
        while head:
            count += 1
            head = head.next
        return count