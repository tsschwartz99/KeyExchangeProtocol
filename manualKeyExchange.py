from keyExchange import *

'''
Problem Combos:
Bob: 54, 27 -> gives (INF)

# alice: cant both be divisible by 2
# could be less than 2^3

# bob: cant both be divisible by 3
# could be less than 3^2
'''

# Alice
m_a = 16
n_a = 65
R_A = CURVE.add(CURVE.dbl_add(P_A, m_a), CURVE.dbl_add(Q_A, n_a))

# Bob 
m_b = 22
n_b = 54
R_B = CURVE.add(CURVE.dbl_add(P_B, m_b), CURVE.dbl_add(Q_B, n_b))

# what alice calculates for first round 
aPhi, aPoints = twoStrategy(R_A, [P_B,Q_B])
E_A = aPhi.codomain

# what bob calculates for first round 
bPhi, bPoints = oddStrategy(R_B, [P_A,Q_A])
E_B = bPhi.codomain
print(E_B)
# what alice calculates for her second round
R_A_prime = E_B.add(E_B.dbl_add(bPoints[0], m_a), E_B.dbl_add(bPoints[1], n_a))
aPhi_prime, aPoints_prime = twoStrategy(R_A_prime,[],E_B)
print(aPhi_prime.codomain.jInvariant())

# what bob calculates for his second round
R_B_prime = E_A.add(E_A.dbl_add(aPoints[0], m_b), E_A.dbl_add(aPoints[1], n_b))
bPhi_prime, bPoints_prime = oddStrategy(R_B_prime,[],E_A)
print(bPhi_prime.codomain.jInvariant())