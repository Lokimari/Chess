from typing import List
import math

# For neatly storing coordinates as class objects
class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, v2):
        return self.x == v2.x and self.y == v2.y

    # Pretty output
    def __str__(self):
        return f"({self.x},{self.y})"

    # Operator Methods
    def __add__(self, v2):
        return Vec2(self.x + v2.x, self.y + v2.y)

    def __sub__(self, v2):
        return Vec2(self.x - v2.x, self.y - v2.y)

    def __mul__(self, num):
        return Vec2(self.x * num, self.y * num)

    # Other
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def round(self):
        return Vec2(round(self.x), round(self.y))

    def normalize(self):
        return Vec2(self.x / self.length(), self.y / self.length())

# Move History (unfinished)
class Move:
    def __init__(self, old, new):
        self.old = old
        self.new = new

    def is_xy(self):
        return (self.new.x != self.old.x and self.new.y == self.old.y or
                self.new.x == self.old.x and self.new.y != self.old.y)

    def is_diagonal(self):
        return (self.old.x - self.old.y == self.new.x - self.new.y) or (self.old.x + self.old.y == self.new.x + self.new.y)

    def direction(self):
        return (self.new - self.old).normalize().round()

    def __str__(self):
        return str(self.old) + " -> " + str(self.new)

    # Shortening data to normalized vector, then getting intermediate spaces & orientation via this process.
    def get_spaces_in_between(self) -> List[Vec2]:
        if not self.is_diagonal() and not self.is_xy():
            return []
        print("NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN")
        num_steps = math.gcd(abs(self.new.x - self.old.x), abs(self.new.y - self.old.y))
        print(num_steps)

        if num_steps <= 1:
            return []
        else:
            direction = (self.new - self.old).normalize().round()
            print(f"{direction}@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            return [self.old + direction * step for step in range(1, num_steps)]
