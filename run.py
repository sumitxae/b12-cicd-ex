import json
import hmac
import hashlib
import requests
from datetime import datetime, timezone
import os

SIGNING_SECRET = os.getenv("SIGNING_SECRET")

payload = {
    "action_run_link": os.getenv("ACTION_RUN_LINK"),
    "email": "sumitxae@gmail.com",
    "name": "Sumit Choudhary",
    "repository_link": os.getenv("REPOSITORY_LINK"),
    "resume_link": "https://drive.google.com/file/d/1tJ-b1hZagepv5-1slPr4X2qZj-h7r0h3/view?usp=sharing",
    "timestamp": datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z"),
}

body = json.dumps(
    payload,
    separators=(",", ":"),
    sort_keys=True,
    ensure_ascii=False,
).encode("utf-8")

signature = hmac.new(
    SIGNING_SECRET.encode("utf-8"),
    body,
    hashlib.sha256,
).hexdigest()

headers = {
    "Content-Type": "application/json",
    "X-Signature-256": f"sha256={signature}",
}

response = requests.post(
    "https://b12.io/apply/submission",
    data=body,
    headers=headers,
)

print("Status Code:", response.status_code)
print("Response:", response.text)

if response.status_code == 200:
    try:
        data = response.json()

        if data.get("success"):
            print("\nSUBMISSION RECEIPT:")
            print(data.get("receipt"))
        else:
            print("Submission failed.")
    except Exception as e:
        print("Could not parse response:", e)
else:
    print("Request failed.")