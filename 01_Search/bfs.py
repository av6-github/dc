from collections import deque

def bfs():
    q = deque([(0, 0)])
    visited = {(0, 0)}

    while q:
        a, b = q.popleft()
        print((a, b))

        if a == 2 or b == 2:
            return

        moves = [
            (3, b), (a, 4),
            (0, b), (a, 0),
            (max(0, a-(4-b)), min(4, a+b)),
            (min(3, a+b), max(0, b-(3-a)))
        ]

        for state in moves:
            if state not in visited:
                visited.add(state)
                q.append(state)

bfs()