from datetime import datetime
from sqlite3 import Connection

class Employee:
    """
    Класс для представления сотрудника.
    """

    def __init__(self, full_name: str, birth_date: str, gender: str) -> None:
        self.full_name: str = full_name
        self.birth_date: datetime = datetime.strptime(birth_date, "%Y-%m-%d")
        self.gender: str = gender

    def calculate_age(self) -> int:
        """
        Рассчитывает возраст сотрудника.
        """
        today = datetime.today()
        age = today.year - self.birth_date.year - (
                    (today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return age

    def save_to_db(self, db_connection: Connection) -> None:
        """
        Сохраняет данные сотрудника в базу данных.
        """
        cursor = db_connection.cursor()
        cursor.execute(
            "INSERT INTO employees (full_name, birth_date, gender, age) VALUES (?, ?, ?, ?)",
            (self.full_name, self.birth_date.strftime("%Y-%m-%d"), self.gender, self.calculate_age())
        )
        db_connection.commit()

    @staticmethod
    def create_table(db_connection: Connection) -> None:
        """
        Создает таблицу сотрудников в базе данных, если она не существует.
        """
        cursor = db_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                birth_date TEXT NOT NULL,
                gender TEXT NOT NULL,
                age INTEGER NOT NULL,
                UNIQUE(full_name, birth_date)
            )
        """)
        db_connection.commit()

    @staticmethod
    def fetch_all(db_connection: Connection):
        """
        Возвращает все записи сотрудников, отсортированные по ФИО.
        """
        cursor = db_connection.cursor()
        cursor.execute("SELECT full_name, birth_date, gender, age FROM employees ORDER BY full_name")
        return cursor.fetchall()

    @staticmethod
    def bulk_insert(db_connection: Connection, employees: list) -> None:
        """
        Пакетная вставка сотрудников в базу данных.
        """
        cursor = db_connection.cursor()
        data = [
            (e.full_name, e.birth_date.strftime("%Y-%m-%d"), e.gender, e.calculate_age())
            for e in employees
        ]
        cursor.executemany(
            "INSERT OR IGNORE INTO employees (full_name, birth_date, gender, age) VALUES (?, ?, ?, ?)",
            data
        )
        db_connection.commit()
