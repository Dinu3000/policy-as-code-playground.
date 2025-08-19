import json
import subprocess
import os
from rego_generator import generate_rego
from policy_merger import merge_policies
from enforcer import enforce_policy

def main():
# Step 1: Generate Rego from English
english_rule = input("Enter plain-English rule (e.g., 'Contractors must never see SSN or salary'): ")
rego_snippet = generate_rego(english_rule)
print(f"Generated Rego: {rego_snippet}"
