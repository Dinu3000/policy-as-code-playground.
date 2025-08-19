def merge_policies(global_policies, tenant_overrides):
    merged = "# Merged Policy\n"
    for name, policy in global_policies.items():
        merged += f"# Global: {name}\n{policy}\n\n"
    for name, override in tenant_overrides.items():
        merged += f"# Tenant Override: {name}\n{override}\n\n"

    merged += """
package enforcement
import data.gdpr
import data.hipaa
# Add more imports...

allow = {
    "decision": global_allow && dept_allow && role_allow && user_allow,
    "reason": "Policy evaluation complete"
}

global_allow { gdpr.allow; hipaa.allow }
dept_allow { input.user.dept != "restricted" }
role_allow { input.user.role in ["admin", "analyst"] }
user_allow { true }

mask_columns := ["ssn", "salary"] if { not allow.decision }
row_filter := "WHERE user_id = current_user()" if { not allow.decision }
"""
    return merged
