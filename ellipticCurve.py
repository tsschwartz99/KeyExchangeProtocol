# global variable
# the field you will mod all numbers by
from numbers import Complex


field = 1

# function to set field
def setField(p):
    global field
    field = p

# function to get field
def getField():
    return field

class Fraction:
    def __init__(self, n, d) -> None:
        self.__numerator = n
        if(d != 0):
            self.__denominator = d
        else:
            self.__denominator = 1 
    
    @property 
    def numerator(self):
        return self.__numerator
    
    @numerator.setter
    def numerator(self, val) -> None:
        self.__numerator = val
    
    @property 
    def denominator(self):
        return self.__denominator
    
    @denominator.setter
    def denominator(self, val) -> None:
        if(val != 0):
            self.__denominator = val

    def __str__(self) -> str:
        return "({})/({})".format(self.numerator, self.denominator)


# a class that will act as complex numbers
class ComplexNumber:

    # a complex number needs to satisfy a+bi
    def __init__(self, real:int, imag:int) -> None:
        p = field
        if(real == None and imag == None):
            self.__a = None
            self.__b = None
        else:
            self.__a = (((real % p) + p) % p)
            self.__b = (((imag % p) + p) % p)

    @property 
    def a(self) -> int:
        return self.__a
    
    @a.setter
    def a(self, val:int) -> None:
        p = field
        self.__a = (((val % p) + p) % p)

    @property 
    def b(self) -> int:
        return self.__b
    
    @b.setter
    def b(self, val:int) -> None:
        p = field
        self.__b = (((val % p) + p) % p)


    # simplifying a fraction, assuming num & den are reals
    def __simplifyFrac(self, f:Fraction) -> int:
        inverse = 0
        p = field
        for i in range(p):
            if(((f.denominator * i) % p) == 1):
                inverse = i
        return (f.numerator * inverse) % p

    def __add__(self, num):
        return ComplexNumber(self.a + num.a, self.b + num.b)

    def __mul__(self, num):
        return ComplexNumber(self.a*num.a - self.b*num.b, self.a*num.b + self.b*num.a)
    
    def __sub__(self,num):
        return ComplexNumber(self.a - num.a, self.b - num.b)

    def __truediv__(self, num):
        den = (num.a)**2 + (num.b)**2
        realNum = self.a*num.a + num.b*self.b 
        imagNum = self.b*num.a - self.a*num.b
        realFrac = Fraction(realNum, den)
        imagFrac = Fraction(imagNum, den)
        return ComplexNumber(self.__simplifyFrac(realFrac), self.__simplifyFrac(imagFrac))
    
    def __eq__(self, num):
        if(self.a == num.a):
            if(self.b == num.b):
                return True
        return False

    # only works for powers >= 1
    def __pow__(self,num):
        val = self
        for x in range(num-1):
            val = self.__mul__(val)
        return val
    
    def __str__(self) -> str:
        return "{} + {}i".format(self.__a,self.__b)

class Point:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
    
    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, val:ComplexNumber):
        self.__x = val

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, val:ComplexNumber):
        self.__y = val

    def __eq__(self, point):
        if(self.x == point.x):
            if(self.y == point.y):
                return True
        return False
    
    def __str__(self):
        if(self.x == ComplexNumber(None,None) and self.y == ComplexNumber(None,None)):
            return "(inf)"
        return "({}, {})".format(self.x.__str__(),self.y.__str__())



class EllipticCurve:

    # point at infinity
    global INF 
    INF = Point(ComplexNumber(None,None),ComplexNumber(None,None))

    def __init__(self, x:ComplexNumber, y:ComplexNumber):
        self.__a = x
        self.__b = y

    @property 
    def a(self) -> ComplexNumber:
        return self.__a
    
    @a.setter
    def a(self, val:ComplexNumber) -> None:
        self.__a = val

    @property 
    def b(self) -> ComplexNumber:
        return self.__b
    
    @b.setter
    def b(self, val:ComplexNumber) -> None:
        self.__b = val    

    def ellipticFunction(self, x:ComplexNumber) -> ComplexNumber:
        return (x*x*x + self.a*x + self.b)

    def add(self, p1:Point, p2:Point) -> Point:
        global lmbda
        global x3 
        global y3

        # p1 + inf = p2
        if(p2 == INF):
            return Point(p1.x,p1.y)
        # p2 + inf = p2
        elif(p1 == INF):
            return Point(p2.x, p2.y)
        elif(not (p1 == p2)):
            # x1 = x2 => inf
            if(p1.x == p2.x):
                return INF
            # calc slope if x1 != x2
            else:
                lambdaNum = p2.y - p1.y 
                lambdaDen = p2.x - p1.x
                lmbda = lambdaNum/lambdaDen
        # p1 = p2
        else:
            # if y = 0 then the tangent line goes to inf 
            if(p1.y == ComplexNumber(0,0)):
                return INF
            # calculate tangent line
            else:
                lambdaNum = ComplexNumber(3,0)*(p1.x * p1.x) + self.__a
                lambdaDen = ComplexNumber(2,0)*p1.y
                lmbda = lambdaNum/lambdaDen
        # create new point
        x3 = lmbda*lmbda - p1.x - p2.x
        y3 = lmbda*(p1.x - x3) - p1.y

        return Point(x3,y3)

    # creates a list of the square roots of y^2 
    def __generateSquares(self):
        sqrList = []
        fieldList = []
        for x in range(field):
            for y in range(field):
                inp = ComplexNumber(x,y)
                fieldList.append(inp)
                sqrList.append(inp*inp)
        return fieldList, sqrList

    # create a list of all points on the curve
    def generatePoints(self):
        ptList = [INF]
        fieldList, sqrList = self.__generateSquares()
        for i in fieldList:
            yy = self.ellipticFunction(i)
            for j in range(len(fieldList)):
                if(yy == sqrList[j]):
                    ptList.append(Point(i,fieldList[j]))
        return ptList

    # double and add 
    def dbl_add(self, pt:Point, num:int):
        # array that will have out num value in it
        array = []
        # array that will have all values
        fullArray = []

        # get the binary equivalent for num
        for i in range(2,len(bin(num))):
            array.append(int(bin(num)[i]))
            fullArray.append(1)

        # set first index as the pt
        fullArray[len(fullArray)-1] = pt

        # generate the full array of all points corresponding to the binary
        i = len(fullArray) - 1
        while i > 0:
            fullArray[i-1] = self.add(fullArray[i], fullArray[i])
            i -= 1
        
        sum = None
        newSum = True
        # add necessary points
        for x in range(len(array)):
            if(array[x] == 1):
                if(newSum):
                    sum = fullArray[x]
                    newSum = False
                else:
                    sum = self.add(sum, fullArray[x])
        return sum

    def jInvariant(self) -> ComplexNumber:
        numerator: ComplexNumber = ComplexNumber(1728*4,0)*self.a**3
        denominator: ComplexNumber = ComplexNumber(4,0)*self.a**3 + ComplexNumber(27,0)*self.b**2
        return numerator/denominator
    
    def __str__(self):
        str = ""
        str += ("E: y^2 = x^3 + ({})x + ({})").format(self.a,self.b)
        return str  

    def points(self):
        str = ""
        str += "\nPoints for E: "
        ptList = self.generatePoints()
        str += "\n{"
        for i in range(len(ptList)-1):
            str += ptList[i].__str__()
            str += ", "
        str += ptList[len(ptList)-1].__str__()
        str += "}"
        str += ("\nNumber of Points: {}").format(len(ptList))
        return str