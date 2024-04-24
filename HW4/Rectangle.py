class Rectangle:
    def __init__(self, length, width):
       self.length = length
       self.width = width
       
    def calculate_area(self):
        return self.length * self.width


rectangle = Rectangle(5,3)

print("Area of 5x3 rectangle:",rectangle.calculate_area())