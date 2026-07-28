import json

import httpx

URL = "http://localhost:8000/tasks"

with open("filtered_data.json", "r") as f:
    tasks = json.load(f)

success = 0
failed = 0

with httpx.Client(timeout=30.0) as client:
    for i, payload in enumerate(tasks, start=1):
        try:
            response = client.post(URL, json=payload)

            if response.status_code in (200, 201):
                success += 1
                print(f"✅ [{i}/{len(tasks)}] {payload['title']}")
            else:
                failed += 1
                print(
                    f"❌ [{i}/{len(tasks)}] {payload['title']} ({response.status_code})"
                )
                print(response.text)

        except Exception as e:
            failed += 1
            print(f"💥 [{i}/{len(tasks)}] {payload['title']}: {e}")

print(f"\nDone. Success: {success}, Failed: {failed}")
