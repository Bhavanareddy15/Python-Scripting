class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
    
    # converts list to linked list
    def build(self, lst):
        head = Node(lst[0])
        curr = head
        for val in lst[1:]:
            curr.next = Node(val)
            curr = curr.next
        return head

    # prints linked list
    def print_list(self, head):
        curr = head
        while curr:
            print(curr.val, end="  ")
            curr = curr.next
        print("None")
    
    def reverse_list(self, head):
        prev = None
        curr = head
        next = None
        while (curr!=None):
            next= curr.next
            curr.next=prev
            prev=curr
            curr = next
        
        head = prev
        return head





ll = LinkedList()
head = ll.build([1, 2, 3, 4, 5])
ll.print_list(head)
head = ll.reverse_list(head)
ll.print_list(head)


