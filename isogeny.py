from ellipticCurve import *

# class that will emulate isogenies
class Isogeny:
    
    # gather information needed to create an isogeny
    # requires an elliptic curve over k and a finite subgroup E(k) of odd order 
    def __init__(self, c: EllipticCurve, sg: list[Point]):
        self.__domain = c
        copy = []
        for x in sg:
            copy.append(x)
        self.__subgroup = copy
        # remove the zero element (INF)
        self.__subgroup.remove(INF)
        self.__order = len(self.__subgroup)
        self.__codomain = self.__calcIsogenousCurve()

    
    # no setters because there shouldn't be a need for them

    # getter methods
    # retrieve the curve the isogeny was constructed from
    # domain
    @property 
    def domain(self) -> EllipticCurve:
        return self.__domain

    @property 
    def subgroup(self) -> list[Point]:
        return self.__subgroup

    @property 
    def order(self) -> int:
        return self.__order   

    # return the isogenous curve
    # codomain
    @property 
    def codomain(self) -> EllipticCurve:
        return self.__codomain
    
    # Velu's theorem
    # given a point find the point on the corresponding curve
    # returns the corresponding point and the isogenous curve
    # rename to evaluate
    def velu(self, p: Point) -> Point:
        if(self.order == 1):
            return self.__twoOrder(p)
        else:
            return self.__oddOrder(p)

    # if subgroup = 2, follow this method
    # Thm. 5.13 (Velu)
    def __twoOrder(self, p: Point) -> tuple[Point,EllipticCurve]:
        r = self.subgroup[0].x
        t: ComplexNumber = ComplexNumber(3,0)*r**2 + self.domain.a
        xVal: ComplexNumber = (p.x**2 - r*p.x + t)/(p.x-r)
        yVal: ComplexNumber = (((p.x-r)**2 - t)/(p.x-r)**2) * p.y
        return Point(xVal,yVal)
    
    # if subgroup order is odd, follow this method
    # Thm. 5.15 (Velu)
    def __oddOrder(self, p: Point) -> Point:
        t: ComplexNumber = ComplexNumber(0,0)
        r_sum: ComplexNumber = ComplexNumber(0,0)
        rp_sum: ComplexNumber = ComplexNumber(0,0)
        for point in self.__subgroup:
            tQ = ComplexNumber(3,0)*(point.x**2) + self.domain.a
            uQ = ComplexNumber(2,0)*(point.y**2)
            t += tQ
            denom = ComplexNumber(1,0)/(p.x-point.x)
            r_sum += (tQ*denom) + (uQ*(denom**2))
            rp_sum += (tQ*(denom**2)) + (ComplexNumber(2,0)*uQ)*(denom**3)
        xVal = p.x + r_sum
        yVal = (ComplexNumber(1,0) - rp_sum) * p.y
        return Point(xVal, yVal)

    # calculate the isogenous elliptic curve

    # calculates the isogenous curve
    def __calcIsogenousCurve(self) -> EllipticCurve:
        t: ComplexNumber
        w: ComplexNumber
        
        if(self.order == 1):
            r = self.subgroup[0].x
            t = ComplexNumber(3,0)*r**2 + self.domain.a
            w = r*t
        else:
            t = ComplexNumber(0,0)
            w = ComplexNumber(0,0)
            for point in self.__subgroup:
                tQ = ComplexNumber(3,0)*(point.x**2) + self.domain.a
                uQ = ComplexNumber(2,0)*(point.y**2)
                wQ = uQ + tQ*point.x
                t += tQ
                w += wQ

        A: ComplexNumber = self.domain.a - ComplexNumber(5,0)*t
        B: ComplexNumber = self.domain.b - ComplexNumber(7,0)*w
        
        return EllipticCurve(A,B)

        
        