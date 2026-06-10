from pathlib import Path
import sys

import duckdb


DB_PATH = "retirement_match_iv.duckdb"


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python scripts/run_sql.py sql/file.sql [sql/file2.sql ...]")

    con = duckdb.connect(DB_PATH)

    for script_arg in sys.argv[1:]:
        script_path = Path(script_arg)
        print(f"Running {script_path}")
        sql = script_path.read_text()
        con.execute(sql)

    con.close()


if __name__ == "__main__":
    main()