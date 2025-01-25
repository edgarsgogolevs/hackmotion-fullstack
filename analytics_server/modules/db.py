from collections.abc import Sequence
import logging
import sqlite3
from contextlib import contextmanager

lg = logging.getLogger("modules.db")

DB_NAME = "database/analytics.db"


@contextmanager
def get_db_connection():
  conn = sqlite3.connect(DB_NAME)
  try:
    yield conn
  finally:
    conn.close()


def insert_dict(table: str, data: dict) -> bool:
  if not data:
    lg.warning("Nothing to insert!")
    return False
  try:
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['?' for _ in data])
    vals = tuple(data.values())

    q = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"

    with get_db_connection() as conn:
      cursor = conn.cursor()
      cursor.execute(q, vals)
      conn.commit()

    lg.debug(f"Successfully inserted data into {table}")
    return True

  except sqlite3.Error as e:
    lg.error(f"Error inserting data into {table}: {str(e)}")
    return False
  except Exception as e:
    lg.error(f"Unexpected error while inserting data into {table}: {str(e)}")
    return False


def select(query: str, values: tuple = tuple()) -> list[dict]:
  if not query.strip().lower().startswith('select'):
    lg.error("Invalid select query!")
    return []

  try:
    with get_db_connection() as conn:
      conn.row_factory = sqlite3.Row
      cursor = conn.cursor()
      cursor.execute(query, values)

      # Convert rows to dictionaries
      rows = [dict(row) for row in cursor.fetchall()]

      lg.debug(f"Successfully executed query: {query} <- {values}")
      return rows

  except sqlite3.Error as e:
    lg.error(f"Database error while executing query: {str(e)}")
    return []
  except Exception as e:
    lg.error(f"Unexpected error while executing query: {str(e)}")
    return []
