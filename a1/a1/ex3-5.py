import math
class Frac:
    def __init__(self, a, b) -> None: 
        c = math.gcd(a, b)
        self.a = a // c
        self.b = b // c
    def __str__(self) -> str:
        return f"{self.a}/{self.b}"

    def averageWith(self, a, b):
        return Frac(self.a * b + a * self.b, self.b * b * 2)
    
    def invert(self):
        if self.a == 1:
            return self.b
        else:
            return str(Frac(self.b, self.a))

a = int(input())
b = int(input())
print(Frac(1, a).averageWith(1, b).invert())