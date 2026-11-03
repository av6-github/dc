# RSA DIGITAL SIGNATURE
p = 61
q = 53

n = p*q
phi = (p-1)*(q-1)

e = 17
d = pow(e, -1, phi)

message = 65

signature = pow(message, d, n)
verified = pow(signature, e, n)

print("Signature:", signature)
print("Verified:", verified == message)

#Elgamal DIGITAL SIGNATURE
from math import gcd

p = 23
g = 5

x = 6
y = pow(g, x, p)

m = 10
k = 7

while gcd(k, p-1) != 1:
    k += 1

r = pow(g, k, p)

s = pow(k, -1, p-1) * (m - x*r) % (p-1)

left = pow(g, m, p)
right = pow(y, r, p) * pow(r, s, p) % p

print("Signature:", r, s)
print("Valid:", left == right)


# DSA
import hashlib

p = 23
q = 11
g = 2

x = 3
y = pow(g, x, p)

m = "HELLO"

h = int(hashlib.sha256(m.encode()).hexdigest(), 16)

k = 4

r = pow(g, k, p) % q

s = pow(k, -1, q) * (h + x*r) % q

print("Signature:", r, s)

w = pow(s, -1, q)

u1 = h * w % q
u2 = r * w % q

v = (pow(g, u1, p) * pow(y, u2, p) % p) % q

print("Valid:", v == r)

# ECDSA

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

import hashlib

G = (5, 1)

n = 19

d = 7
Q = scalar_mult(d, G)

message = "HELLO"

h = int(hashlib.sha256(message.encode()).hexdigest(), 16)

k = 3

R = scalar_mult(k, G)

r = R[0] % n

s = pow(k, -1, n) * (h + d*r) % n

print("Signature:", r, s)

w = pow(s, -1, n)

u1 = h * w % n
u2 = r * w % n

R2 = point_add(
    scalar_mult(u1, G),
    scalar_mult(u2, Q)
)

v = R2[0] % n

print("Valid:", v == r)