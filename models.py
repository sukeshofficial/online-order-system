from database import get_db

class DBModels:

    @staticmethod
    def create_tables():
        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS menu(
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                price FLOAT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS orders(
                id INT AUTO_INCREMENT PRIMARY KEY,
                item_id INT,
                quantity INT,
                total FLOAT,
                payment_status VARCHAR(20) DEFAULT 'Pending',
                FOREIGN KEY (item_id) REFERENCES menu(id)
            )
        """)

        conn.commit()
        conn.close()
