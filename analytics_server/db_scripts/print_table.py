import sqlite3
import sys


if __name__ == "__main__":
  table = sys.argv[1]
  conn = sqlite3.connect("database/analytics.db")

  cur = conn.cursor()
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()
  cursor.execute(f"SELECT * FROM {table}")

  # Convert rows to dictionaries
  rows = [dict(row) for row in cursor.fetchall()]

  print(rows)
