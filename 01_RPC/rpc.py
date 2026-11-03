import csv
import json 

def processData(value):
    print(f"[SERVER EXECUTION] Processing parameter: {value}")
    return f"Processed data: {value}"

def validateData(value):
    print(f"[SERVER EXECUTION] Validating parameter: {value}")
    if 0 <= value <= 500:
        return "VALID"
    else:
        return "INVALID"
    
def updateSignal(value):
    print(f"[SERVER EXECUTION] Updating signal with parameter: {value}")
    if 0 <= value <= 250:
        return "Signal updated to 100 seconds"
    else:
        return "Signal updated to 200 seconds"
    
def server_dispatcher(marshalled_request):
    request = json.loads(marshalled_request)
    method = request["method_name"]
    parameter = int(request["param_value"])
    remote_methods = {
        "processData": processData,
        "validateData": validateData,
        "updateSignal": updateSignal
    }
    if method not in remote_methods:
        return "invalid method"
    return remote_methods[method](parameter)

def rpc_client(filename):
    with open(filename, newline="") as file:
        for row in csv.DictReader(file):
            print(f"[DISPATCH] {row["client_name"]} invoking method {row["method_name"]}")
            request = {
                "call_id": row["call_id"],
                "client_name": row["client_name"],
                "method_name": row["method_name"],
                "param_value": row["param_value"],
                "timestamp": row["timestamp"]
            }

            marshalled_request = json.dumps(request)
            print(f"[MARSHALLING] {marshalled_request}")

            result = server_dispatcher(marshalled_request)
            print(f"[RETURN] {result}")

if __name__ == "__main__":
    rpc_client("rpc.csv")