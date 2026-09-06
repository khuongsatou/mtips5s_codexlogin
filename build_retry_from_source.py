import os
import sqlite3
from pathlib import Path


SOURCE_PATH = Path("/Users/apple/.codex/attachments/0e399d2d-e9f3-4f2d-a8d4-7793ff16179e/pasted-text.txt")
DB_PATH = Path(os.path.expanduser("~/.9router/db/data.sqlite"))
OUTPUT_PATH = Path(__file__).with_name("accounts_retry_failed_and_unrun.txt")


def email_key(value):
    return value.strip().rstrip(".").lower()


def main():
    source_lines = []
    seen_source = set()
    for raw_line in SOURCE_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split("|")
        if len(fields) < 2 or not fields[0].strip() or not fields[1].strip():
            continue
        fields[0] = email_key(fields[0])
        normalized = "|".join(fields[:3])
        if fields[0] not in seen_source:
            seen_source.add(fields[0])
            source_lines.append(normalized)

    db = sqlite3.connect(DB_PATH)
    successful = {
        email_key(row[0])
        for row in db.execute(
            "SELECT email FROM providerConnections WHERE provider='codex' AND isActive<>0"
        )
        if row[0]
    }
    db.close()

    retry_lines = [line for line in source_lines if email_key(line.split("|", 1)[0]) not in successful]
    OUTPUT_PATH.write_text(
        "# Retry list: failed and not-yet-successful accounts from the supplied source list.\n"
        "# Format: email|password|2fa_secret\n"
        + "\n".join(retry_lines)
        + "\n",
        encoding="utf-8",
    )
    print(f"source_unique={len(source_lines)} successful_removed={len(source_lines)-len(retry_lines)} retry={len(retry_lines)}")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()
