import csv
import threading
import time

mutex = threading.Lock()
completed_tasks = []

def worker(task):
    name = task["thread_name"]
    task_id = task["task_id"]
    delay = int(task["burst_ms"])/1000

    print(f"[{name}] started processing {task_id}")
    time.sleep(delay)
    print(f"[{name}] finished processing; waiting for mutex")

    with mutex:
        print(f"[{name}] LOCK ACQUIRED to record {task_id}")
        completed_tasks.append(task_id)
        print(f"[{name}] LOCK RELEASED")
    
def main():
    with open("multithreading.csv", newline="") as file:
        tasks = list(csv.DictReader(file))

    threads = []
    for task in tasks:
        thread = threading.Thread(target=worker, args=(task,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    
    print("[SUMMARY] all threads have finished")
    print("[COMPLETED TASKS]", ", ".join(completed_tasks))

if __name__ == "__main__":
    main()