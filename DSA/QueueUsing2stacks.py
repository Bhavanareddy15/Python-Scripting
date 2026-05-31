class Queue:
    def __init__(self):
        self.stack1 = []
        self.stack2 = []
    
    def enqueue(self, x):
        self.stack1.append(x)

    def dequeue(self):
        if self.is_empty():
            print("Queue is empty")
            return
        if not self.stack2:          # only pour when stack2 is empty
            while self.stack1:
                self.stack2.append(self.stack1.pop())  # pour and clear stack1
        return self.stack2.pop() 
    
    def peek(self):
        if self.is_empty():
            print("Queue is empty")
            return
        if not self.stack2:          # only pour when stack2 is empty
            while self.stack1:
                self.stack2.append(self.stack1.pop())  # pour and clear stack1
        return self.stack2[-1]
        
    def is_empty(self):
        if len(self.stack2)==0 and len(self.stack1)==0:
            return True
        else:
            return False

        


q = Queue()
q.enqueue(1)
q.enqueue(2)
q.enqueue(3)
print(q.peek())      # 1
print(q.dequeue())   # 1
print(q.dequeue())   # 2
print(q.is_empty())  # False
print(q.dequeue())   # 3
print(q.is_empty())  # True
q.dequeue()          # Queue is empty
        