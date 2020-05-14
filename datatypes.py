from typing import List
import math

# For neatly storing coordinates as class objects
class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x},{self.y})"

    def __add__(self, v2):
        return Vec2(self.x + v2.x, self.y + v2.y)

    def __sub__(self, v2):
        return Vec2(self.x - v2.x, self.y - v2.y)

    def __mul__(self, num):
        return Vec2(self.x * num, self.y * num)

    def round(self):
        return Vec2(round(self.x), round(self.y))

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    # then div len by its own len
    def normalize(self):
        return Vec2(self.x / self.length(), self.y / self.length())

# Move History (unfinished)
class Move:
    def __init__(self, old, new):
        self.old = old
        self.new = new

    def __str__(self):
        return str(self.old) + " -> " + str(self.new)

    def get_spaces_inbetween(self) -> List[Vec2]:
        num_steps = math.gcd(self.new.x - self.old.x, self.new.y - self.new.y)

        if num_steps <= 1:
            return []
        else:
            direction = (self.new - self.old).normalize().round()
            return [self.old + direction * step for step in range(1, num_steps)]
