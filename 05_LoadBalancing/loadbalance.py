import csv
from collections import defaultdict

WORKERS = ["Worker_1", "Worker_2", "Worker_3"]

def distribute_jobs(filename):
    loads = defaultdict(int)
    counts = defaultdict(int)
    assignments = []

    with open(filename, newline="") as file:
        jobs = list(csv.DictReader(file))
    
    for job in jobs:
        worker = min(WORKERS, key=lambda w: (loads[w], counts[w], w))
        units = int(job["compute_units"])
        loads[worker] += units
        counts[worker] += 1

        job["assigned_worker"] = worker
        job["status"] = "ASSIGNED"
        assignments.append(job)
        print(f"[ALLOCATE] {job["job_id"]} ({units} units) -> {worker}")
    
    print("[LOAD SUMMARY]")
    for worker in WORKERS:
        print(f"{worker}: {counts[worker]} jobs, {loads[worker]} compute units")

    with open("output.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "job_id", "compute_units", "assigned_worker", "status"
        ])
        writer.writeheader()
        writer.writerows(assignments)
    
if __name__ == "__main__":
    distribute_jobs("loadbalance.csv")