# Key exchange will take place over TCP client/ server
# Alice will serve as the client
# use ipconfig -> IPv4 Address of server computer

import sys
from keyExchange import *
from socket import *
import pickle

# global variable for client_socket
# open socket
client_socket = socket(AF_INET, SOCK_STREAM)

# this function will take in the command line arguments and connect to the server
def getArgs():
    # take in the command line arguments
    server_ip = sys.argv[1]
    server_port = sys.argv[2]
    
    # Error Handling
    try:
        client_socket.connect((server_ip,int(server_port)))

    # if the ports don't match, the program will quit
    except TimeoutError:
        print("Error: Incorrect port number or IP address.")
        quit()

    except ConnectionRefusedError:
        print("Error: Incorrect port number or IP address.")
        quit()

# function to get user's secret keys
# question: will not take 0 as a number ... is this okay?
def getKeysHelper() -> tuple[int,int]:
    print()
    print("INPUT YOUR SECRET KEYS.\nTHEY MUST BE BETWEEN 1 AND 8, INCLUSIVE.\nM AND N CANNOT BOTH BE EVEN.")
    
    # obtain values from user
    m: int = int(input("M VALUE: "))

    # check that m is valid
    while(m>9 or m<1):
        print("M MUST BE BETWEEN 1 AND 8, INCLUSIVE.")
        m = int(input("M VALUE: "))

    n: int = int(input("N VALUE: "))

    # check that n is valid
    while(n>9 or n<1 or (m%2 == 0 and n%2 == 0)):
        print("N MUST BE BETWEEN 1 AND 8, INCLUSIVE.\nM AND N CANNOT BOTH BE EVEN.")
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
    rPoint = CURVE.add(CURVE.dbl_add(P_A, m), CURVE.dbl_add(Q_A, n))
    print() 

    return (m,n,rPoint)
    
# this function will send information to the server
def send(tuple):
    # encode and send away whatever tuple
    serialized_tuple = pickle.dumps(tuple)
    client_socket.send(serialized_tuple)

# function to receive message from Bob
def receive()->tuple[Isogeny,list[Point]]:
    # receive all the packets that bob is sending
    data = b""
    while True:
        packet = client_socket.recv(2048)
        if not packet: break
        data += packet
    
    # decoded tuple is the received decoded and results in a tuple
    decoded_tuple = pickle.loads(data)
    return decoded_tuple

# main function
def main():
    getArgs()
    m, n, R = getKeys()
    
    # this tuple contains the isogeny [0] and the list of isogenous points [1]
    isogenyTuple = twoStrategy(R, [P_B,Q_B])
    send(isogenyTuple)
    
    # this is the isogeny [0] and isogenous points [1] Alice receives from Bob
    bobIsogenyTuple = receive()
    bobIsogeny = bobIsogenyTuple[0]
    bobPoints = bobIsogenyTuple[1]

    # E_B is Bob's isogenous curve
    E_B = bobIsogeny.codomain

    # calculate new R point from Bob's curve/points
    R_prime = E_B.add(E_B.dbl_add(bobPoints[0], m), E_B.dbl_add(bobPoints[1], n))

    # create a new isogeny
    phi, _ = twoStrategy(R_prime,[],E_B)
    print("Your shared secret key is: " + str(phi.codomain.jInvariant()))
    
    client_socket.close()

#### MAIN FUNCTION CALL ####
main()