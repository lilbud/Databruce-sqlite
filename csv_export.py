"""
Project Name: Databruce
Author Name: Lilbud
Name: CSV Export
File Purpose: Exports all tables in database to CSV files
"""

import os
import sqlite3
import pandas as pd

os.makedirs("_csv", exist_ok=True)

conn = sqlite3.connect(os.path.dirname(__file__) + "/_database/database.sqlite")
cur = conn.cursor()

def csv_export():
    """Exports all Tables to CSV files"""

    for t in cur.execute("""SELECT name FROM sqlite_master WHERE type='table';"""):
        if "sequence" not in t[0]:
            pd.read_sql_query(f"SELECT * FROM {t[0]}", conn).to_csv(f'_csv/{t[0]}.csv', index=False)
            
            print(f"{t[0]} table exported to {t[0]}.csv")

csv_export()
