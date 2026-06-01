class MinStack:
    def __init__(self):
        self.stack=[]
        self.min_stack=[]
    
    def push(self, x):
        self.stack.append(x)
        if self.min_stack:
            self.min_stack.append(min(x, self.min_stack[-1]))  # compare with current min
        else:
            self.min_stack.append(x)  # first element, just push
    
    def pop(self):
        if self.stack:
            self.min_stack.pop()
            return self.stack.pop()
        else:
            return("Stack is empty")
    
    def top(self):
        if self.stack:
            return self.stack[-1]
        else:
            return("Stack is empty")
    
    def get_min(self):
        if self.stack:
            return self.min_stack[-1]
        else:
            return("Stack is empty")
    
s = MinStack()
s.push(5)
s.push(3)
s.push(7)
s.push(2)
print(s.get_min())   # 2
print(s.top())       # 2
s.pop()
print(s.get_min())   # 3  ← min updated after pop!
s.pop()
print(s.get_min())   # 3
s.pop()
print(s.get_min())   # 5