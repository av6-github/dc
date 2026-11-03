import csv
from concurrent.futures import ThreadPoolExecutor

def read_matrix(filename):
    matrix = []
    with open(filename, newline="") as file:
        for row in csv.DictReader(file):
            matrix.append([int(row[f"col_{i}"]) for i in range(4)])
    return matrix

def multiply_row(row_index, row, matrix_b):
    print(f"[WORKER {row_index}] Computing assigned row")
    result = []
    for col in range(len(matrix_b[0])):
        value = sum(row[k] * matrix_b[k][col] for k in range(len(row)))
        result.append(value)
    return row_index, result

def main():
    matrix_a = read_matrix("matrix_22.csv")

    # The chit specifies one 4-column matrix CSV, not a second matrix.
    # For a complete reproducible multiplication, use B = transpose(A).
    matrix_b = [list(col) for col in zip(*matrix_a)]

    print("[MASTER] Matrix A loaded from CSV.")
    print("[MASTER] Matrix B is constructed as transpose(A), since the chit specifies only one matrix CSV.")
    print("[MASTER] Scattering rows to worker tasks...")

    results = [None] * len(matrix_a)
    with ThreadPoolExecutor(max_workers=len(matrix_a)) as executor:
        futures = [
            executor.submit(multiply_row, i, row, matrix_b)
            for i, row in enumerate(matrix_a)
        ]
        for future in futures:
            row_index, result_row = future.result()
            results[row_index] = result_row
            print(f"[MASTER] Gathered result row {row_index}: {result_row}")

    print("\n[FINAL MATRIX PRODUCT: A x A^T]")
    for row in results:
        print(row)

if __name__ == "__main__":
    main()
