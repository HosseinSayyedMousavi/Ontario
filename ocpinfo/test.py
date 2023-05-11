import sqlite3
conn = sqlite3.connect('book.db')
cursor = conn.cursor()
cursor.execute("SELECT site_id FROM book_cfi_ir")
site_ids = cursor.fetchall()
print(site_ids)
input()