from collections import deque

N = 4
W = (1, 3)
G = (2, 3)
P = {(3, 1), (3, 3), (4, 4)}

safe = {(1, 1)}
visited = set()


def nbr(x):
    r, c = x
    return [(r+dr, c+dc) for dr,dc in
            [(1,0),(-1,0),(0,1),(0,-1)]
            if 1 <= r+dr <= N and 1 <= c+dc <= N]


def perceive(x):
    p = set()

    if W in nbr(x): p.add("Stench")
    if any(n in P for n in nbr(x)): p.add("Breeze")
    if x == G: p.add("Glitter")

    return p


def bfs(start, goal):
    q = deque([[start]])
    seen = {start}

    while q:
        path = q.popleft()

        if path[-1] == goal:
            return path

        for n in nbr(path[-1]):
            if n in safe and n not in seen:
                seen.add(n)
                q.append(path + [n])


pos = (1, 1)

while True:

    # Perceive
    p = perceive(pos)
    print("At", pos, ":", p or "Nothing")
    visited.add(pos)

    # Knowledge / inference
    if "Breeze" not in p and "Stench" not in p:
        safe.update(nbr(pos))

    safe -= P
    safe.discard(W)

    # Gold found
    if "Glitter" in p:
        print("GOLD FOUND!")

        path = bfs(pos, (1, 1))
        print("Return:", path)
        break

    # Find an unexplored safe cell
    targets = safe - visited

    if not targets:
        print("No safe cells left!")
        break

    target = next(iter(targets))

    # Move using BFS
    path = bfs(pos, target)

    if not path:
        print("No safe path!")
        break

    pos = path[-1]

print("SUCCESS!")