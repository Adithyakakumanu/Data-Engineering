import requests

def generate_sql(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "sqlcoder",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()
    return data["response"].strip()