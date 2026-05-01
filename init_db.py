import sqlite3
import os

os.makedirs('instance', exist_ok=True)
conn = sqlite3.connect('instance/database.db')
conn.executescript(open('database/schema.sql', encoding='utf-8').read())
conn.commit()
conn.close()
print('DB init OK')
