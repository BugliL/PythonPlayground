from enum import IntEnum
from enum import Enum

class X(Enum):
    A = 1
    B = 2
    C = 3
    D = 0

    def __gt__(self, other):
        return self.value > other.value

print(X(max(X)).value)
