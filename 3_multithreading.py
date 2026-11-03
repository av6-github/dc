# RSA

from math import gcd

p = 61
q = 53

n = p * q
phi = (p-1) * (q-1)

e = 17
d = pow(e, -1, phi)

print("Public key:", e, n)
print("Private key:", d, n)

M = 65
C = pow(M, e, n)
print("Cipher:", C)

M2 = pow(C, d, n)
print("Plain:", M2)

# Diffie-Hellman

p = 23
g = 5

a = 6
b = 15

A = pow(g, a, p)
B = pow(g, b, p)

KA = pow(B, a, p)
KB = pow(A, b, p)

print(A, B)
print(KA, KB)

# Elgamal

p = 23
g = 5

x = 6
y = pow(g, x, p)

m = 10
k = 3

c1 = pow(g, k, p)
c2 = m * pow(y, k, p) % p

s = pow(c1, x, p)
m2 = c2 * pow(s, -1, p) % p

print("Public:", p, g, y)
print("Cipher:", c1, c2)
print("Plain:", m2)

# ECC (y^2 = x^3 + ax + b (mod p))
p = 17
a = 2
b = 2

O = None

def point_add(P, Q):
    if P is None:
        return Q

    if Q is None:
        return P

    x1, y1 = P
    x2, y2 = Q

    # P + (-P) = O
    if x1 == x2 and (y1 + y2) % p == 0:
        return None

    if P != Q:
        m = (y2 - y1) * pow(x2 - x1, -1, p) % p
    else:
        m = (3*x1*x1 + a) * pow(2*y1, -1, p) % p

    x3 = (m*m - x1 - x2) % p
    y3 = (m*(x1 - x3) - y1) % p

    return (x3, y3)

def scalar_mult(k, P):
    R = None

    while k:
        if k & 1:
            R = point_add(R, P)

        P = point_add(P, P)
        k >>= 1

    return R

# ECDH
G = (5, 1)

alice_private = 5
bob_private = 7

A = scalar_mult(alice_private, G)
B = scalar_mult(bob_private, G)

alice_shared = scalar_mult(alice_private, B)
bob_shared = scalar_mult(bob_private, A)

print("Alice public:", A)
print("Bob public:", B)

print("Shared:", alice_shared, bob_shared)

#EC-Elgamal
G = (5, 1)

d = 5
Q = scalar_mult(d, G)

M = (6, 3)
k = 7

C1 = scalar_mult(k, G)

C2 = point_add(
    M,
    scalar_mult(k, Q)
)

print("Cipher:", C1, C2)

def point_neg(P):
    if P is None:
        return None

    x, y = P
    return (x, (-y) % p)

temp = scalar_mult(d, C1)

M2 = point_add(C2, point_neg(temp))

print("Original:", M)
print("Decrypted:", M2)