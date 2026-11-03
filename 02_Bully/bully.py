import csv

def read_nodes(filename):
    nodes = []
    with open(filename, newline="") as file:
        for row in csv.DictReader(file):
            nodes.append({
                "id" : int(row["node_id"]),
                "alive" : row["is_alive"].strip().upper()=="TRUE",
                "coordinator": row["is_current_coordinator"].strip().upper()=="TRUE"
            })
    return nodes

def bully(nodes):
    # 1. Coordinator Detection
    coordinators = [n for n in nodes if n["coordinator"]]
    old_coordinator = coordinators[0]
    print(f"[DETECTION] current coordinator is node {old_coordinator['id']}")
    if old_coordinator["alive"]:
        print("[STATUS] current coordinator is alive no need for election")
        return
    print("[STATUS] current coordinator is dead, starting election")

    # 2, Alive Node Detection
    alive_nodes = [n for n in nodes if n["alive"]]
    initiator = min(alive_nodes, key=lambda n: n["id"])
    print(f"[ELECTION] node {initiator['id']} is initiating election")

    # 3. Election Process
    higher_nodes = [n for n in alive_nodes if n["id"] > initiator["id"]]
    if not higher_nodes:
        winner = initiator
    else:
        for node in higher_nodes:
            print(f"[ELECTION] node {initiator['id']} -> node {node["id"]}: ELECTION")
            print(f"[RESPONSE] node {node["id"]} -> node {initiator["id"]}: OK")
        winner = max(higher_nodes, key=lambda n: n["id"])
    print(f"[COORDINATOR] Node {winner['id']} broadcasts COORDINATOR.")

    # 4. Coordinator Announcement
    for node in alive_nodes:
        if node["id"] != winner["id"]:
            print(f"[COORDINATOR] Node {winner['id']} -> node {node['id']}: COORDINATOR")

if __name__ == "__main__":
    nodes = read_nodes("bully.csv")
    bully(nodes)
