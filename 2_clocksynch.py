# CAESAR CIPHER
def caesar(text, k):
    result = ""
    for c in text:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            result += chr((ord(c)-base+k) % 26 + base)
        else:
            result += c
    return result

# MONOALPHABETIC CIPHER
plain = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
key = "QWERTYUIOPASDFGHJKLZXCVBNM"

def monoalphabetic(text):
    result = ""
    for c in text.upper():
        if c in plain:
            result += key[plain.index(c)]
        else:
            result += c
    return result

def monoalphabetic_decrypt(text):
    result = ""
    for c in text.upper():
        if c in key:
            result += plain[key.index(c)]
        else:
            result += c
    return result

print(monoalphabetic_decrypt("ITSSG"))

# VIGENERE CIPHER
def vigenere(text, key):
    result = ""
    key = key.upper()
    j = 0

    for c in text.upper():
        if c.isalpha():
            p = ord(c) - 65
            k = ord(key[j % len(key)]) - 65
            result += chr((p+k) % 26 + 65)
            j += 1
        else:
            result += c
    return result

def vigenere_decrypt(text, key):
    result = ""
    key = key.upper()
    j = 0
    for c in text.upper():
        if c.isalpha():
            p = ord(c) - 65
            k = ord(key[j % len(key)]) - 65
            result += chr((p-k) % 26 + 65)
            j += 1
        else:
            result += c
    return result

print(vigenere_decrypt("LXFOPV", "LEMON"))
# PLAYFAIR CIPHER
def playfair_matrix(key):
    key = key.upper().replace("J", "I")
    chars = ""

    for c in key + "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if c not in chars:
            chars += c

    return [list(chars[i:i+5]) for i in range(0, 25, 5)]

def playfair_encrypt(text, key):
    m = playfair_matrix(key)

    pos = {}
    for r in range(5):
        for c in range(5):
            pos[m[r][c]] = (r, c)

    text = text.upper().replace("J", "I")
    text = ''.join(c for c in text if c.isalpha())

    pairs = []
    i = 0

    while i < len(text):
        a = text[i]

        if i + 1 == len(text):
            b = 'X'
            i += 1
        elif text[i] == text[i+1]:
            b = 'X'
            i += 1
        else:
            b = text[i+1]
            i += 2

        pairs.append((a, b))

    result = ""

    for a, b in pairs:
        r1, c1 = pos[a]
        r2, c2 = pos[b]

        if r1 == r2:
            result += m[r1][(c1+1)%5]
            result += m[r2][(c2+1)%5]

        elif c1 == c2:
            result += m[(r1+1)%5][c1]
            result += m[(r2+1)%5][c2]

        else:
            result += m[r1][c2]
            result += m[r2][c1]

    return result

def playfair_decrypt(text, key):
    m = playfair_matrix(key)

    pos = {}
    for r in range(5):
        for c in range(5):
            pos[m[r][c]] = (r, c)

    text = text.upper().replace("J", "I")
    result = ""

    for i in range(0, len(text), 2):
        a = text[i]
        b = text[i+1]

        r1, c1 = pos[a]
        r2, c2 = pos[b]

        if r1 == r2:
            result += m[r1][(c1-1)%5]
            result += m[r2][(c2-1)%5]

        elif c1 == c2:
            result += m[(r1-1)%5][c1]
            result += m[(r2-1)%5][c2]

        else:
            result += m[r1][c2]
            result += m[r2][c1]

    return result

cipher = playfair_encrypt("HELLO", "MONARCHY")
print(cipher)
print(playfair_decrypt(cipher, "MONARCHY"))

# HILL CIPHER 2 BY 2
def hill2_encrypt(text, K):
    text = text.upper().replace(" ", "")

    if len(text) % 2:
        text += "X"

    result = ""

    for i in range(0, len(text), 2):
        p1 = ord(text[i]) - 65
        p2 = ord(text[i+1]) - 65

        c1 = (K[0][0]*p1 + K[0][1]*p2) % 26
        c2 = (K[1][0]*p1 + K[1][1]*p2) % 26

        result += chr(c1+65) + chr(c2+65)

    return result


K = [[3, 3],
     [2, 5]]

print(hill2_encrypt("HELP", K))

def hill2_decrypt(text, K):
    a, b = K[0]
    c, d = K[1]

    det = (a*d - b*c) % 26
    det_inv = pow(det, -1, 26)

    invK = [
        [d*det_inv % 26, -b*det_inv % 26],
        [-c*det_inv % 26, a*det_inv % 26]
    ]

    return hill2_encrypt(text, invK)


K = [[3, 3],
     [2, 5]]

cipher = hill2_encrypt("HELP", K)

print(cipher)
print(hill2_decrypt(cipher, K))

# HILL CIPHER 3 BY 3
def hill3_encrypt(text, K):
    text = text.upper().replace(" ", "")

    while len(text) % 3:
        text += "X"

    result = ""

    for i in range(0, len(text), 3):

        P = [ord(text[i+j])-65 for j in range(3)]

        for r in range(3):
            value = sum(K[r][c] * P[c] for c in range(3))
            result += chr(value % 26 + 65)

    return result


K = [
    [6, 24, 1],
    [13, 16, 10],
    [20, 17, 15]
]

print(hill3_encrypt("ACT", K))

def hill3_decrypt(text, K):

    det = (
        K[0][0]*(K[1][1]*K[2][2] - K[1][2]*K[2][1])
        - K[0][1]*(K[1][0]*K[2][2] - K[1][2]*K[2][0])
        + K[0][2]*(K[1][0]*K[2][1] - K[1][1]*K[2][0])
    )

    det %= 26
    det_inv = pow(det, -1, 26)

    invK = [[0]*3 for _ in range(3)]

    invK[0][0] = (K[1][1]*K[2][2] - K[1][2]*K[2][1])
    invK[0][1] = -(K[0][1]*K[2][2] - K[0][2]*K[2][1])
    invK[0][2] = (K[0][1]*K[1][2] - K[0][2]*K[1][1])

    invK[1][0] = -(K[1][0]*K[2][2] - K[1][2]*K[2][0])
    invK[1][1] = (K[0][0]*K[2][2] - K[0][2]*K[2][0])
    invK[1][2] = -(K[0][0]*K[1][2] - K[0][2]*K[1][0])

    invK[2][0] = (K[1][0]*K[2][1] - K[1][1]*K[2][0])
    invK[2][1] = -(K[0][0]*K[2][1] - K[0][1]*K[2][0])
    invK[2][2] = (K[0][0]*K[1][1] - K[0][1]*K[1][0])

    for i in range(3):
        for j in range(3):
            invK[i][j] = invK[i][j] * det_inv % 26

    return hill3_encrypt(text, invK)


K = [
    [6, 24, 1],
    [13, 16, 10],
    [20, 17, 15]
]

cipher = hill3_encrypt("ACT", K)

print(cipher)
print(hill3_decrypt(cipher, K))

#RAIL FENCE
def rail_fence_encrypt(text, rails):
    rows = [''] * rails
    row = 0
    direction = 1

    for c in text:
        rows[row] += c

        if row == 0:
            direction = 1
        elif row == rails-1:
            direction = -1

        row += direction

    return ''.join(rows)


print(rail_fence_encrypt("HELLOWORLD", 3))

def rail_fence_decrypt(text, rails):
    pattern = list(range(rails)) + list(range(rails-2, 0, -1))

    positions = [pattern[i % len(pattern)] for i in range(len(text))]

    counts = [positions.count(i) for i in range(rails)]

    rows = []
    start = 0

    for count in counts:
        rows.append(list(text[start:start+count]))
        start += count

    result = ""

    for r in positions:
        result += rows[r].pop(0)

    return result


cipher = rail_fence_encrypt("HELLOWORLD", 3)

print(cipher)
print(rail_fence_decrypt(cipher, 3))

# COLUMNAR TRANSPOSITION

def columnar_encrypt(text, key):
    text = text.replace(" ", "").upper()

    cols = len(key)
    rows = (len(text) + cols - 1) // cols

    text += 'X' * (rows * cols - len(text))

    grid = [
        text[i:i+cols]
        for i in range(0, len(text), cols)
    ]

    order = sorted(range(cols), key=lambda i: key[i])

    result = ""

    for c in order:
        for r in range(rows):
            result += grid[r][c]

    return result


print(columnar_encrypt("HELLOWORLD", "ZEBRA"))

def columnar_decrypt(text, key):
    cols = len(key)
    rows = len(text) // cols

    order = sorted(range(cols), key=lambda i: key[i])

    grid = [[''] * cols for _ in range(rows)]

    k = 0

    for c in order:
        for r in range(rows):
            grid[r][c] = text[k]
            k += 1

    result = ""

    for r in range(rows):
        for c in range(cols):
            result += grid[r][c]

    return result.rstrip('X')


cipher = columnar_encrypt("HELLOWORLD", "ZEBRA")

print(cipher)
print(columnar_decrypt(cipher, "ZEBRA"))

# VERNAM/ONE-TIME PAD CIPHER
def vernam(text, key):
    return ''.join(
        chr(ord(a) ^ ord(b))
        for a, b in zip(text, key)
    )


cipher = vernam("HELLO", "XMCKL")
print(cipher)

print(vernam(cipher, "XMCKL"))