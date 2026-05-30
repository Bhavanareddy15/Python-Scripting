from abc import ABC, abstractmethod

class Employee(ABC):
    def __init__(self, name, salary):
        self.name = name
        self.__salary= salary

    @abstractmethod
    def get_details(self):
        return(f"Employee: {self.name}, Salary: {self.__salary}")
    
    def get_salary(self):
        return self.__salary
    
    def set_salary(self, salary):
        if salary > 0:
            self.__salary = salary
        else:
            print("Invalid salary")

    


class Manager(Employee):
    def __init__(self, name, salary, department):
        super().__init__(name, salary)  # calls Employee's constructor
        self.department = department    # then add Manager's own variable

    def get_details(self):
        return f"Manager: {self.name}, Salary: {self.get_salary()}, Department: {self.department}"

class Intern(Employee):
    def __init__(self, name, salary, duration):
        super().__init__(name, salary)
        self.duration= duration
    
    def get_details(self):
        return f"Intern: {self.name}, Salary: {self.get_salary()}, Duration: {self.duration} months"


def print_all_details(staff):
    for employee in staff:
        st = employee.get_details()
        print(st)

'''
# Test: Inheritance and Overriding
e = Employee("Alice", 50000)
print(e.get_details())
# Employee: Alice, Salary: 50000

m = Manager("Bob", 80000, "Engineering")
print(m.get_details())
# Manager: Bob, Salary: 80000, Department: Engineering
'''
'''
#Polymorphism
staff = [
    Employee("Alice", 50000),
    Manager("Bob", 80000, "Engineering"),
    Intern("Charlie", 10000, 6)
]
print_all_details(staff)

#encapsulation
e = Employee("Alice", 50000)
print(e.get_salary())    # 50000'''

staff = [
    Manager("Bob", 80000, "Engineering"),
    Intern("Charlie", 10000, 6)
]
print_all_details(staff)

