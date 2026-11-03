import csv

def synchronize(filename):
    with open(filename, newline="") as file:
        for row in csv.DictReader(file):
            client = row["client_id"]
            t0 = float(row["t0_send_ms"])
            server_time = float(row["t_server_ms"])
            t1 = float(row["t1_recv_ms"])

            rtt = t1 - t0
            estimated_server_time = server_time + (rtt/2)
            offset = estimated_server_time - t1

            print(f"\n[CLIENT {client}]")
            print(f"RTT = T1 - T0 = {t1} - {t0} = {rtt:.2f} ms")
            print(f"Estimated server time = {server_time} + ({rtt:.2f}/2) = {estimated_server_time:.2f} ms")
            print(f"Client clock offset = {offset:+.2f} ms")
            print(f"Adjusted client time = {estimated_server_time:.2f} ms")


if __name__ == "__main__":
    synchronize("christian.csv")