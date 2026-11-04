def state_space(a, b, path):
    print((a, b))

    if a == 2 or b == 2:
        return True

    moves = [
        (3, b), (a, 4),     # fill
        (0, b), (a, 0),     # empty
        (max(0, a-(4-b)), min(4, a+b)),  # 3 -> 4
        (min(3, a+b), max(0, b-(3-a)))   # 4 -> 3
    ]

    for x, y in moves:
        if (x, y) not in path:
            if state_space(x, y, path + [(x, y)]):
                return True

state_space(0, 0, [(0, 0)])