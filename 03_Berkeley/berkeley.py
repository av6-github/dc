import csv

def read_clocks(filename):
    nodes = []
    with open(filename, newline="") as file:
        for row in csv.DictReader(file):
            nodes.append({
                "id" : row["node_id"],
                "time" : float(row["clock_time_sec"]),
                "faulty": row["is_faulty"].strip().upper()=="TRUE"
            })
    return nodes

def berkeley(nodes):
    print("[MASTER] Polling node clocks....")
    valid = []
    for node in nodes:
        print(f"[POLLING] {node["id"]} with time = {node["time"]}")
        if node["faulty"]:
            print(f"[DISCARD] {node["id"]} marked faulty; excluded")
        else:
            valid.append(node)
    
    average_time = sum(n["time"] for n in valid) / len(valid)
    print(f"[MASTER] average time: {average_time} seconds")
    print("[ADJUSTMENTS]")
    for node in valid:
        offset = average_time - node["time"]
        direction = "advance" if offset >= 0 else "slow down"
        print(f"{node["id"]}: {direction} by {abs(offset)} seconds")

if __name__ == "__main__":
    berkeley(read_clocks("berkeley.csv"))