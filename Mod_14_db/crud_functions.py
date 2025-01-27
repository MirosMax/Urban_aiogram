import sqlite3


connection = sqlite3.connect('tg_bot.db')
cursor = connection.cursor()


def initiate_db():
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')

    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INT NOT NULL,
    balance INTEGER NOT NULL
    )
    ''')

    connection.commit()


def add_products(list_products):
    for product in list_products:
        cursor.execute(f'INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
                       (product['title'], product['description'], product['price']))

    connection.commit()


def get_all_products():
    cursor.execute(f'SELECT * FROM Products')
    result = cursor.fetchall()

    return result




initiate_db()
vitamin_supplements = [
    {
        "title": "Витамин C 1000 мг",
        "description": "Высокая дозировка витамина C для поддержания иммунной системы.",
        "price": 450
    },
    {
        "title": "Комплекс Омега-3",
        "description": "Жирные кислоты Омега-3 для здоровья сердца и сосудов.",
        "price": 850
    },
    {
        "title": "Витамин D3 2000 МЕ",
        "description": "Поддержка костей и иммунной системы.",
        "price": 600
    },
    {
        "title": "Мультивитамины для мужчин",
        "description": "Комплекс витаминов и минералов, разработанный специально для мужчин.",
        "price": 750
    },
    {
        "title": "Мультивитамины для женщин",
        "description": "Комплекс витаминов и минералов, разработанный специально для женщин.",
        "price": 750
    },
    {
        "title": "Витамин B12 500 мкг",
        "description": "Поддержка нервной системы и энергии.",
        "price": 400
    },
    {
        "title": "Кальций + Магний",
        "description": "Поддержка костей и мышц.",
        "price": 550
    },
    {
        "title": "Витамин E 400 МЕ",
        "description": "Антиоксидантная поддержка и здоровье кожи.",
        "price": 500
    },
    {
        "title": "Цинк 50 мг",
        "description": "Поддержка иммунной системы и здоровья кожи.",
        "price": 350
    },
    {
        "title": "Комплекс для суставов",
        "description": "Глюкозамин, хондроитин и МСМ для поддержки суставов.",
        "price": 900
    }
]
# add_products(vitamin_supplements)

all_products = get_all_products()

connection.close()




