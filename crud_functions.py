import sqlite3

def initiate_db():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL
    )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL,
            balance INTEGER NOT NULL
        )
        ''')
    cursor.execute("SELECT COUNT(*) FROM Products")
    if cursor.fetchone()[0] == 0:
        example_products = [
            ("Продукт 1", "Описание 1", 100),
            ("Продукт 2", "Описание 2", 200),
            ("Продукт 3", "Описание 3", 300),
            ("Продукт 4", "Описание 4", 400),
        ]
        cursor.executemany("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)", example_products)

    conn.commit()
    conn.close()

def get_all_products():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    cursor.execute("SELECT title, description, price FROM Products")
    products = cursor.fetchall()

    conn.close()
    return products

def add_user(username, email, age):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
                   (username, email, age, 1000))

    conn.commit()
    conn.close()


def is_included(username):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Users WHERE username = ?", (username,))
    count = cursor.fetchone()[0]

    conn.close()
    return count > 0

