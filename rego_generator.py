import openai
openai.api_key = "your-openai-key"

def generate_rego(english_rule):
    prompt = f"""
Convert this plain-English governance rule to a Rego policy snippet for OPA.
Example: "Contractors must never see SSN or salary" -> "package access\nallow {{ input.user.role != \\"contractor\\" or input.data.type not in [\\"ssn\\", \\"salary\\"] }}"
Rule: {english_rule}
Output only the Rego code, no explanations.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
