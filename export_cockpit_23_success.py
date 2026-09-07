import json
import os
import sqlite3


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATUS_PATH = "/tmp/auto_status.json"
DB_PATH = os.path.expanduser("~/.9router/db/data.sqlite")
OUTPUT_PATH = os.path.join(BASE_DIR, "cockpit-import-23-success-20260906.json")


def main():
    status = json.load(open(STATUS_PATH, encoding="utf-8"))
    emails = [
        item["email"].strip().lower()
        for item in status.get("results", [])
        if item.get("status") == "success" and item.get("email")
    ]
    if len(emails) != 23:
        raise RuntimeError(f"Expected 23 successful accounts, found {len(emails)}")

    db = sqlite3.connect(DB_PATH)
    records = []
    seen = set()
    for email in emails:
        row = db.execute(
            "SELECT email, updatedAt, data FROM providerConnections "
            "WHERE provider = 'codex' AND isActive <> 0 AND lower(email) = ? "
            "ORDER BY updatedAt DESC LIMIT 1",
            (email,),
        ).fetchone()
        if not row:
            raise RuntimeError(f"Successful account not found in SQLite: {email}")
        actual_email, updated_at, raw_data = row
        key = actual_email.strip().lower()
        if key in seen:
            continue
        seen.add(key)
        data = json.loads(raw_data or "{}")
        provider_data = data.get("providerSpecificData") or {}
        record = {
            "id_token": data.get("idToken") or "",
            "access_token": data.get("accessToken") or "",
            "refresh_token": data.get("refreshToken") or "",
            "account_id": provider_data.get("chatgptAccountId") or "",
            "last_refresh": data.get("lastUsedAt") or updated_at or "",
            "email": actual_email,
            "type": "codex",
            "expired": data.get("expiresAt") or "",
        }
        if not record["refresh_token"]:
            raise RuntimeError(f"Missing refresh token: {actual_email}")
        records.append(record)
    db.close()

    if len(records) != 23:
        raise RuntimeError(f"Expected 23 unique records, found {len(records)}")
    with open(OUTPUT_PATH, "w", encoding="utf-8") as output:
        json.dump(records, output, ensure_ascii=False, indent=2)
        output.write("\n")
    print(f"Exported {len(records)} accounts to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
