import sqlite3


db = sqlite3.connect('users.db')

cursor = db.cursor()
#sq   lite

#increment - kobeyiw
cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
phone_number TEXT NOT NULL,
adress TEXT NOT NULL,
age INTEGER NOT NULL,
user_id INTEGER NOT NULL,
username TEXT NOT NULL
)

''')
#qosiw,oshiriw,shigariw
#CRUD - CREATE READ UPDATE DELETE

async def save_user(name, phone_number, adress, age, user_id, username):
    cursor.execute('''
INSERT INTO users(name, phone_number, adress, age, user_id, username)
VALUES(?,?,?,?,?,?)
''', (name, phone_number, adress, age, user_id, username))
    db.commit()



async def get_user_id():
    cursor.execute('SELECT user_id FROM users')
    datas = cursor.fetchall()
    return datas




