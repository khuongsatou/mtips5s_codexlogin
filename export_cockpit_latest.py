import json
import os
import sqlite3


DB_PATH = os.path.expanduser("~/.9router/db/data.sqlite")
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cockpit-import-27-new.json")
LIMIT = 27


def main():
    db = sqlite3.connect(DB_PATH)
    rows = db.execute(
        """
        SELECT id, email, updatedAt, data
        FROM providerConnections
        WHERE provider = 'codex' AND isActive <> 0
        ORDER BY updatedAt DESC
        LIMIT ?
        """,
        (LIMIT,),
    ).fetchall()
    db.close()

    records = []
    seen = set()
    for connection_id, email, updated_at, raw_data in rows:
        email_key = (email or "").strip().lower()
        if not email_key or email_key in seen:
            continue
        seen.add(email_key)
        data = json.loads(raw_data or "{}")
        provider_data = data.get("providerSpecificData") or {}
        records.append(
            {
                "id_token": data.get("idToken") or "",
                "access_token": data.get("accessToken") or "",
                "refresh_token": data.get("refreshToken") or "",
                "account_id": provider_data.get("chatgptAccountId") or "",
                "last_refresh": data.get("lastUsedAt") or updated_at or "",
                "email": email or "",
                "type": "codex",
                "expired": data.get("expiresAt") or "",
            }
        )

    if len(records) != LIMIT:
        raise RuntimeError(f"Expected {LIMIT} unique active accounts, found {len(records)}")
    if any(not item["refresh_token"] for item in records):
        raise RuntimeError("At least one selected account has no refresh token")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as output:
        json.dump(records, output, ensure_ascii=False, indent=2)
        output.write("\n")
    print(f"Exported {len(records)} accounts to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
