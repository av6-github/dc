bases = [69, 28, 62, 15, 13]

# FERMATS TEST
def fermat(n, bases):
    for a in bases:
        if pow(a, n-1, n) != 1:
            return False
    return True

# EULERS TEST
def euler(n, bases):
    for a in bases:
        r = pow(a, (n-1)//2, n)
        if r != 1 and r != n-1:
            return False
    return True

# MILLER-RABIN TEST
def miller_rabin(n, bases):
    d = n-1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in bases:
        a = a % n
        if a == 0:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n-1:
            continue
        composite = True
        for _ in range(s-1):
            x = pow(x, 2, n)
            if x == n-1:
                composite = False
                break
        if composite:
            return False
    return True

# CHINESE REMAINDER THEOREM
def crt(a, m):
    M = 1
    for x in m:
        M *= x

    result = 0

    for ai, mi in zip(a, m):
        Mi = M // mi
        result += ai * Mi * pow(Mi, -1, mi)

    return result % M


a = [2, 3, 2]
m = [3, 5, 7]

print(crt(a, m))