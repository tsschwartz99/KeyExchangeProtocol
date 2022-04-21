from ellipticCurve import *
from isogeny import *
from parameterSet import *

# set the field to the proper prime number
setField(PRIME)

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
