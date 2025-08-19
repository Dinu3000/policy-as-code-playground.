import json
import subprocess
import os
from rego_generator import generate_rego
from policy_merger import merge_policies
from enforcer import enforce_policy, compile_to_wasm

def main():
    # Step 1: Generate Rego from English
    english_rule = input("Enter plain-English rule (e.g., 'Contractors must never see SSN or salary'): ")
    rego_snippet = generate_rego(english_rule)
    print(f"Generated Rego: {rego_snippet}")

    # Step 2: Merge with global policies
    global_policies = {
        "gdpr": "package gdpr\nallow { input.user.role != \"contractor\" }",
        "hipaa": "package hipaa\nallow { input.data.pii == false }"
    }
    tenant_overrides = {"custom": rego_snippet}
    merged_rego = merge_policies(global_policies, tenant_overrides)
    with open("merged_policy.rego", "w") as f:
        f.write(merged_rego)
    print("Merged Rego saved to merged_policy.rego")

    # Step 3: Compile to WASM
    compile_to_wasm("merged_policy.rego", "policy.wasm")
    print("Compiled to policy.wasm")

    # Step 4: Enforce (simulate Snowflake query)
    context = {
        "user": {"role": "contractor", "dept": "hr"},
        "data": {"pii": True, "query": "SELECT * FROM sensitive_table"}
    }
    result = enforce_policy("policy.wasm", context)
    print(f"Enforcement Result: {json.dumps(result, indent=2)}")

if __name__ == "__main__":
    main()
