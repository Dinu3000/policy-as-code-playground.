import subprocess
import json

def compile_to_wasm(rego_file, wasm_file):
    subprocess.run(["opa", "build", "-t", "wasm", "-e", "enforcement/allow", rego_file, "-o", wasm_file])

def enforce_policy(wasm_file, input_context):
    input_json = json.dumps({"input": input_context})
    result = subprocess.run(
        ["opa", "eval", "-t", "wasm", "-d", wasm_file, "-i", "-", "data.enforcement.allow"],
        input=input_json.encode(), capture_output=True, text=True
    )
    output = json.loads(result.stdout)

    return {
        "allow": output["result"]["decision"],
        "reason": output["result"]["reason"],
        "mask_columns": output["result"].get("mask_columns", []),
        "row_filter": output["result"].get("row_filter", "")
    }
