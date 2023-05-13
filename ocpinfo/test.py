import sqlite3
conn = sqlite3.connect('Pharmacy.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM Pharmacy.db")
site_ids = cursor.fetchall()
print(site_ids)
input()