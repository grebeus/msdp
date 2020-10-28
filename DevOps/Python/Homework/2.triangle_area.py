from sys import argv
from math import sqrt

a = int(argv[1])
b = int(argv[2])
c = int(argv[3])

p = (a + b + c) / 2
S = sqrt(p * (p - a) * (p - b) * (p - c))

print(S)
