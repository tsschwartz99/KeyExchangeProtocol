from ellipticCurve import *
from isogeny import *
from parameterSet import *

# set the field to the proper prime number
setField(PRIME)

# Alice
m_a = 10
n_a = 39
R_A = CURVE.add(CURVE.dbl_add(P_A, m_a), CURVE.dbl_add(Q_A, n_a))

# Bob 
m_b = 22
n_b = 15
R_B = CURVE.add(CURVE.dbl_add(P_B, m_b), CURVE.dbl_add(Q_B, n_b))

# function to create subgroups
# shouldnt reference CURVE
def createSubgroup(c:EllipticCurve, p:Point) -> list[Point]:
    temp = p
    sg = []
    while(not(temp == INF)):
        # add the point to the list
        sg.append(temp)
        # add temp and p together to get the next point
        temp = c.add(temp,p)
    # add the point at infinity
    sg.append(temp)
    return sg

# function to implement the strategy for a 2 order point
def twoStrategy(p:Point, evalList: list[Point] = [], c: EllipticCurve = CURVE) -> tuple[Isogeny, list[Point]]:
    phi: Isogeny = None
    curve: EllipticCurve = c
    point: Point = p
    for p in range(PRIME_A-1,-1,-1):
        subgroup: list[Point] = createSubgroup(curve, curve.dbl_add(point,2**p))
        phi = Isogeny(curve,subgroup)
        curve = phi.codomain
        point = phi.velu(point)
        evalList = list(map(phi.velu,evalList))
    return (phi, evalList)

# function to implement the strategy for an odd order point
def oddStrategy(p:Point, evalList: list[Point] = [], c: EllipticCurve = CURVE) -> tuple[Isogeny, list[Point]]:
    phi: Isogeny = None
    curve: EllipticCurve = c
    point: Point = p
    for p in range(PRIME_B-1,-1,-1):
        subgroup: list[Point] = createSubgroup(curve, curve.dbl_add(point,3**p))
        phi = Isogeny(curve,subgroup)
        curve = phi.codomain
        point = phi.velu(point)
        evalList = list(map(phi.velu,evalList))
    return (phi, evalList)

# what alice calculates for first round 
aPhi, aPoints = twoStrategy(R_A, [P_B,Q_B])
E_A = aPhi.codomain

# what bob calculates for first round 
bPhi, bPoints = oddStrategy(R_B, [P_A,Q_A])
E_B = bPhi.codomain

# what alice calculates for her second round
R_A_prime = E_B.add(E_B.dbl_add(bPoints[0], m_a), E_B.dbl_add(bPoints[1], n_a))
aPhi_prime, aPoints_prime = twoStrategy(R_A_prime,[],E_B)
print(aPhi_prime.codomain.jInvariant())

# what bob calculates for her second round
R_B_prime = E_A.add(E_A.dbl_add(aPoints[0], m_b), E_A.dbl_add(aPoints[1], n_b))
bPhi_prime, bPoints_prime = oddStrategy(R_B_prime,[],E_A)
print(bPhi_prime.codomain.jInvariant())
