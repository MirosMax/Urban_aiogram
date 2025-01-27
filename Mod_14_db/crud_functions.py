import sqlite3


def initiate_db(name_db, name_table):
    connection = sqlite3.connect(name_db)
    cursor = connection.cursor()

    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {name_table}(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')

    connection.commit()
    connection.close()


def add_products(list_products, name_db, name_table):
    connection = sqlite3.connect(name_db)
    cursor = connection.cursor()

    for product in list_products:
        cursor.execute(f'INSERT INTO {name_table} (title, description, price) VALUES (?, ?, ?)',
                       (product['title'], product['description'], product['price']))

    connection.commit()
    connection.close()


def get_all_products(name_db, name_table):
    connection = sqlite3.connect(name_db)
    cursor = connection.cursor()

    cursor.execute(f'SELECT * FROM {name_table}')
    all_products = cursor.fetchall()

    connection.commit()
    connection.close()

    return all_products


if __name__ == '__main__':
    initiate_db('not_telegram.db', 'Products')
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
    # add_products(vitamin_supplements, 'not_telegram.db', 'Products')






