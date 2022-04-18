from ellipticCurve import *

# the prime numbers that construct the field prime
PRIME_A = 3
PRIME_B = 2

# the field prims
PRIME = 2**PRIME_A * 3**PRIME_B - 1
setField(PRIME)

# the supersingular elliptic curve
CURVE = EllipticCurve(ComplexNumber(-11,0), ComplexNumber(14,0))

# the points and subgroups for Alice
P_A = Point(ComplexNumber(18,37),ComplexNumber(57,32))
Q_A = Point(ComplexNumber(41,63),ComplexNumber(17,13))

# the points and subgroups for Bob 
P_B = Point(ComplexNumber(41,7),ComplexNumber(60,12))
Q_B = Point(ComplexNumber(58,6),ComplexNumber(50,56))