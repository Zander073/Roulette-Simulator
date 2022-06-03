
class Pocket:
    def __init__(self, number, color):
        self.number = number
        self.color = color

    # Returns the number of a pocket
    def get_number(self):
        return self.number

    # Returns the color of a pocket
    def get_color(self):
        return self.color
    
    # Returns both attributes as a tuple
    def get_pocket(self):
        return (self.number, self.color)
