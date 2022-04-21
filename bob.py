# Key exchange will take place over TCP client/ server
# Bob will serve as the server

from keyExchange import *
from socket import *
import pickle

# global socket variable
server_socket = socket(AF_INET, SOCK_STREAM)

# function to get user's secret keys
# question: will not take 0 as a number ... is this okay?
def getKeysHelper() -> tuple[int,int]:
    print("INPUT YOUR SECRET KEYS.\nTHEY MUST BE BETWEEN 1 AND 70, INCLUSIVE.")
    
    # obtain values from user
    m: int = int(input("M VALUE: "))

    # check that m is valid
    while(m>70 or m<1):
        print("M MUST BE BETWEEN 1 AND 70, INCLUSIVE.")
        m = int(input("M VALUE: "))

    n: int = int(input("N VALUE: "))

    # check that n is valid
    while(n>70 or n<1):
        print("N MUST BE BETWEEN 1 AND 70, INCLUSIVE.")
        n = int(input("N VALUE: "))

    # return m and n
    return (m,n)
    
# function to get user's secret key and ensure correct input
def getKeys() -> tuple[int,int, Point]:
    while(True):
        try:
            m, n = getKeysHelper()
            break
        except:
            print("\nERROR: INVALID INPUT.\nTRY AGAIN.\n")

    # this point will be the generator for the subgroup
    rPoint = CURVE.add(CURVE.dbl_add(P_B, m), CURVE.dbl_add(Q_B, n))

    return (m,n,rPoint)

# function that sets up the server socket
def setUp():
    server_socket.bind(('',12000))
    # have the socket for the server listen
    server_socket.listen(1)
    print("Bob is ready to exchange keys.\n")

# function to send tuple to Alice
def send(tuple, s: socket):
    # encode and send away whatever tuple
    buffers=[]
    serialized_tuple = pickle.dumps(tuple)
    s.send(serialized_tuple)

# function to receive tuple from Alice
def receive() -> tuple[tuple[Isogeny,list[Point]], socket]:
    connection_socket, address = server_socket.accept()
    
    # receive all the packets coming from Alice     
    request = connection_socket.recv(2048)
    recieved_tuple = pickle.loads(request)

    return (recieved_tuple, connection_socket)

# main function
def main():   
    # get private keys and R
    m, n, R = getKeys()

    # set up the socket and listen    
    setUp()

    # aliceIsogenyTuple is the isogeny [0] and isogenous points [1] Alice receives from Bob
    # connection_socket is the socket that we will send info back to
    (aliceIsogenyTuple, connection_socket) = receive()
    
    # Alice's isogeny and pointList
    aliceIsogeny = aliceIsogenyTuple[0]
    alicePoints = aliceIsogenyTuple[1]

    # this tuple contains the isogeny [0] and the list of isogenous points [1]
    isogenyTuple = oddStrategy(R, [P_A,Q_A])
    
    # send isogenyTuple to Alice
    send(isogenyTuple,connection_socket)

    # E_A is Alice's isogenous curve
    E_A = aliceIsogeny.codomain

    # calculate new R point from Bob's curve/points
    R_prime = E_A.add(E_A.dbl_add(alicePoints[0], m), E_A.dbl_add(alicePoints[1], n))

    # create a new isogeny
    phi, _ = oddStrategy(R_prime,[],E_A)
    print(phi.codomain.jInvariant())

    connection_socket.close()

#### MAIN FUNCTION CALL ####
main()