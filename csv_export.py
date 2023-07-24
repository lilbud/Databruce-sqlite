"""
Project Name: Databruce
Author Name: Lilbud
Name: CSV Export
File Purpose: Exports all tables in database to CSV files
"""

import pandas as pd
import os, sqlite3

conn = sqlite3.connect(os.path.dirname(__file__) + "/_database/database.sqlite")
cur = conn.cursor()

def csv_export():
	tableList = cur.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
	for t in tableList:
		if "sequence" not in t[0]:
			pd.read_sql_query("SELECT * FROM " + t[0], conn).to_csv('_csv/' + t[0].lower() + '.csv', index=False)

	print("exported to csv")
	
csv_export()