def valid_par(inp):
    par_dict={'(':')', '{':'}', '[': ']'}
    stack= []
    for char in inp:
        if char in par_dict:
            stack.append(char)
        else:
            if not stack:
                return False
            poppedElement = stack.pop()
            if par_dict[poppedElement]==char:
                temp=1
            else: 
                return False
    return len(stack) == 0


inp = "([{}])"
print(valid_par(inp))