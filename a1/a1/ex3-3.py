class Frac:
    def __init__(self, a, b) -> None: 
        self.a = a
        self.b = b
    def __str__(self) -> str:
        return f"{self.a}/{self.b}"

    def averageWith(self, other):
        return Frac(self.a * other.a, self.b * other.b)
    
    def invert(self):
        if self.a == 1:
            return self.b
        else:
            return str(Frac(self.b, self.a))

a = int(input())
b = int(input())
print(Frac(1, a).averageWith(1, b).invert())