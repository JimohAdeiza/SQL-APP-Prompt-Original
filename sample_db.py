
import sqlite3

conn = sqlite3.connect("sample.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS merchants (
    id INTEGER PRIMARY KEY,
    name TEXT,
    onboarded_date DATE,
    location TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    merchant_id INTEGER,
    amount REAL,
    date DATE,
    FOREIGN KEY (merchant_id) REFERENCES merchants(id)
)
""")

cursor.execute("DELETE FROM merchants")
cursor.execute("DELETE FROM transactions")

merchants = [
    (1, 'ShopEasy', '2025-01-10', 'Lagos'),
    (2, 'MarketPro', '2025-02-05', 'Abuja'),
    (3, 'QuickBuy', '2025-03-15', 'Kano')
]

transactions = [
    (1, 1, 1200.50, '2025-04-01'),
    (2, 2, 850.00, '2025-04-02'),
    (3, 1, 500.00, '2025-04-05'),
    (4, 3, 400.00, '2025-04-10')
]

cursor.executemany("INSERT INTO merchants VALUES (?, ?, ?, ?)", merchants)
cursor.executemany("INSERT INTO transactions VALUES (?, ?, ?, ?)", transactions)

conn.commit()
conn.close()
