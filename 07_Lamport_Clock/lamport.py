import csv

clocks = {}
messages = []
results = []

with open("lamport.csv", newline="") as file:
    events = list(csv.DictReader(file))

for event in events:
    eid = event["event_id"]
    process = event["process_id"]
    event_type = event["event_type"]
    target = event["message_to"]

    if process not in clocks:
        clocks[process] = int(event["initial_clock"])

    if event_type == "RECEIVE":
        for message in messages:
            if message[0] == target and message[1] == process:
                clocks[process] = max(clocks[process], message[2]) + 1
                messages.remove(message)
                break
    else:
        clocks[process] += 1

        if event_type == "SEND":
            messages.append((process, target, clocks[process]))

    results.append((clocks[process], eid, process))

    print(f"{eid} ({process}) -> {clocks[process]}")


print("\n[CAUSAL ORDER]")

for time, eid, process in sorted(results):
    print(f"{time}: {eid} ({process})")