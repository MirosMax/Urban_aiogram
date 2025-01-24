import sqlite3


connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

cursor.execute('CREATE INDEX IF NOT EXISTS idx_email ON Users (email)')

# # Удаление из базы запись с id = 6
# cursor.execute('DELETE FROM Users WHERE id == ?', (6,))

# Подсчет всех записей БД
cursor.execute('SELECT COUNT(*) FROM Users')
count = cursor.fetchone()[0]

# Сумма балансов
cursor.execute('SELECT SUM(balance) FROM Users')
sum_balance = cursor.fetchone()[0]

# Средний баланс
print(sum_balance / count)

connection.commit()
connection.close()