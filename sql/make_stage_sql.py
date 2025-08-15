#!/usr/bin/env python3
import sys, csv, re
from pathlib import Path

if len(sys.argv) < 3:
    print("usage: make_stage_sql.py <csv_path> <staging_table_name> [schema=stg]")
    sys.exit(1)

csv_path = Path(sys.argv[1])
table = sys.argv[2]
schema = sys.argv[3] if len(sys.argv) > 3 else "stg"

with csv_path.open('r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    headers = next(reader)

seen = set()
cols = []
for h in headers:
    # sanitize to valid SQL identifiers
    name = re.sub(r'[^a-zA-Z0-9_]', '_', h.strip()).lower()
    if not name or name[0].isdigit():
        name = f"col_{name}"
    base = name
    i = 1
    while name in seen:
        i += 1
        name = f"{base}_{i}"
    seen.add(name)
    cols.append(f'  "{name}" TEXT')

print(f"DROP TABLE IF EXISTS {schema}.{table};")
print(f"CREATE UNLOGGED TABLE {schema}.{table} (")
print(",\n".join(cols))
print(");")

