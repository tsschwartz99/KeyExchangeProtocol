from keyExchange import *

'''
Problem Combos:
Bob: 54, 27 -> gives (INF)
'''

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