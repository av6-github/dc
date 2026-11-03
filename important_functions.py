def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a%b)
 
def egcd(a,b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a%b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return None
    return x % m

def power(a, b, m):
    return pow(a, b, m)