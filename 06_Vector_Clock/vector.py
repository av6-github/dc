import csv

PROCESSES = ["P1", "P2", "P3"]

def less_than(a, b):
    return all(x <= y for x, y in zip(a, b)) and a != b

def main():
    clocks = {
        "P1": [0,0,0],
        "P2": [0, 0, 0],
        "P3": [0, 0, 0]
    }

    messages = []
    event_vectors = {}

    with open("vector.csv", newline="") as file:
        events = list(csv.DictReader(file))
    
    for event in events:
        event_id = event["event_id"]
        process = event["process_id"]
        action = event["event_action"].upper()
        target = event["target_process"]

        index = PROCESSES.index(process)

        if action == "RECEIVE":
            for message in messages:
                if message[0] == target and message[1] == process:
                    received_vector = message[2]
                    for i in range(3):
                        clocks[process][i] = max(clocks[process][i], received_vector[i])
                    messages.remove(message)
                    break
        clocks[process][index] += 1

        if action == "SEND":
            messages.append(
                (process, target, clocks[process].copy())
            )  

        event_vectors[event_id] = clocks[process].copy()

        print(f"{event_id} ({process}, {action}) -> {event_vectors[event_id]}")   

    # causuality comparision

    ids = list(event_vectors.keys())
    for i in range(len(ids)):
        for j in range(i+1, len(ids)):
                a = event_vectors[ids[i]]
                b = event_vectors[ids[j]]

                if less_than(a, b):
                    print(f"{ids[i]} -> {ids[j]}")
                elif less_than(b, a):
                    print(f"{ids[j]} -> {ids[i]}")
                else:
                    print(f"{ids[i]} || {ids[j]}")

if __name__ == "__main__":
    main()