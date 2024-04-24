class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        
    def increase_salary(self, percent):
        self.salary += (self.salary * (percent/100))
        
        
employee = Employee("John", 5000)

employee.increase_salary(10)

print("Updated salary of", employee.name,"--", employee.salary)