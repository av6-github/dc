import csv

def main():
    nodes = {}
    with open("ring.csv", newline="") as file:
        for row in csv.DictReader(file):
            node_id = int(row["node_id"])
            nodes[node_id] = {
                "next": int(row["next_node_id"]),
                "active": row["is_active"].strip().upper()=="TRUE",
                "priority": int(row["priority_rank"])
            }

    current = min(nodes)
    visited = set()
    token_ids = []

    while current not in visited:
        visited.add(current)
        
        node = nodes[current]
        if node["active"]:
            token_ids.append(current)
            print(f"[TOKEN] election token visited active node {current}")
        else:
            print(f"[SKIP] Node {current} is inactive")
        
        current = node["next"]

    winner = max(token_ids)
    print(f"[RESULT] highest active node ID is node {winner}")
    print(f"[COORDINATOR] Node {winner} is elected as the new coordinator")

if __name__ == "__main__":
    main()