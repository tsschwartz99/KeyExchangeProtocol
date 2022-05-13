# KeyExchangeProtocol
The study of Elliptic Curves continues to reveal more secure and efficient methods to encrypt information. For example, in De Feo, Jao, and Plut’s paper "Towards Quantum-Resistant Cryptosystems From Supersingular Elliptic Curve Isogenies", they provide an abstract key exchange protocol using isogonies on supersingular elliptic curves. The main idea of this code is to present an accurate manifestation of the abstract protocol constructed by De Feo et al., which will be realized using Python. This protocol is founded in the Diffie-Hellman algorithm using isogenies on supersingular elliptic curves as its primary operation.

Contents required for running the protocol:
- alice.py
    -> This is the client file for the key exchange protocol. Must be run after bob.py has been established, and requires two command-line arguments: IP address (of server) and port number (hardcoded) 
- bob.py
    -> This is the server for the key exchange protocol. Must be run before alice.py.
- ellipticCurve.py
    -> A class file containing the classes Fraction, ComplexNumber, Point, and EllipticCurve.
- isogeny.py
    -> A class file containing the Isogeny class.
- keyExchange.py
    -> A helper file containing some functions that perform strategy-related opertations. Essentially, this file aides in the actual key exchange process between Alice and Bob.
- manualKeyExchange.py
    -> A file that runs the key exchange without implementing the computer networking aspect of this project.
- parameterSet.py
    -> A file containing constants that are used as the parameters for this key exchange.

A demonstration video and the accompanying research paper also are included in this repository.

A huge thank-you to Dr. Aaron Hutchinson and Dr. Stacey McAdams for aiding me in my first attempt at performing research.