from models import Employee
from database import get_db_connection
import random
import time
from typing import Optional
from utils import export_calculation,export_to_file


class EmployeeService:
    """
    Сервис для управления сотрудниками в базе данных.
    """

    FIRST_NAMES = {
        "Male": ["Ivan", "Petr", "Alex", "Max", "Anton", "Pavel", "Mark", "Stanislav", "Sergey"],
        "Female": ["Anna", "Maria", "Elena", "Olga", "Natalia", "Ekaterina", "Irina", "Tatiana", "Svetlana"]
    }
    MIDDLE_NAMES = {
        "Male": ["Sergeevich", "Petrovich", "Alexandrovich", "Mikhailovich", "Nikolaevich"],
        "Female": ["Sergeevna", "Petrovna", "Alexandrovna", "Mikhailovna", "Nikolaevna"]
    }
    LAST_NAMES = {
        "Male": ["Ivanov", "Petrov", "Sidorov", "Fedorov", "Semenov"],
        "Female": ["Ivanova", "Petrova", "Sidorova", "Fedorova", "Semenova"]
    }

    def __init__(self) -> None:
        self.db_connection = get_db_connection()
        self.optimized: bool = False
        self.first_query_time: Optional[float] = None

    def create_table(self) -> None:
        """
        Создает таблицу сотрудников в базе данных.
        """
        Employee.create_table(self.db_connection)

    def create_employee(self, full_name: str, birth_date: str, gender: str) -> None:
        """
        Создает запись сотрудника и сохраняет её в базе данных.
        """
        employee = Employee(full_name, birth_date, gender)
        employee.save_to_db(self.db_connection)

    def generate_bulk_data(self, num_employees: int) -> None:
        """
        Генерирует данные сотрудников и массово вставляет их в базу.
        """
        employees = [
            Employee(
                self.generate_random_name(gender := random.choice(["Male", "Female"])),
                self.generate_random_birth_date(),
                gender,
            )
            for _ in range(num_employees)
        ]

        employees.extend(
            Employee(
                self.generate_fixed_male_name(),
                self.generate_random_birth_date(),
                "Male"
            )
            for _ in range(100)
        )

        Employee.bulk_insert(self.db_connection, employees)
        print(f"Generated {num_employees + 100} employee records.")

    def generate_random_name(self, gender: str) -> str:
        """
        Генерирует случайное ФИО на основе пола.
        """
        return f"{random.choice(self.LAST_NAMES[gender])} {random.choice(self.FIRST_NAMES[gender])} {random.choice(self.MIDDLE_NAMES[gender])}"

    def generate_fixed_male_name(self) -> str:
        """
        Генерирует фиксированное ФИО с фамилией, начинающейся на 'F'.
        """
        return "Fedorov {} {}".format(random.choice(self.FIRST_NAMES['Male']), random.choice(self.MIDDLE_NAMES['Male']))

    def generate_random_birth_date(self) -> str:
        """
        Генерирует случайную дату рождения в формате YYYY-MM-DD.
        """
        return f"{random.randint(1950, 2000)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"

    def fetch_employees_by_criteria(self) -> None:
        """
        Выбирает сотрудников 'Male' с фамилией, начинающейся на 'F'
        (записывает список сотрудников в файл employees_f_male.txt),
         измеряет время выполнения
         (записывает время в файл query_performance.txt)
        """
        cursor = self.db_connection.cursor()
        start_time = time.time()

        cursor.execute(
            "SELECT full_name, birth_date, gender FROM employees WHERE gender = 'Male' AND full_name LIKE 'F%' LIMIT 1000"
        )
        employees = cursor.fetchall()

        self.query_time = time.time() - start_time
        export_calculation(self.query_time)

        if employees:
            export_to_file(employees, "employees_f_male.txt")
        else:
            print("No employees found matching the criteria.")

        cursor.close()

    def show_all_employees(self) -> None:
        """
        Выводит все уникальные записи сотрудников, отсортированные по ФИО и дате рождения,
        с расчетом возраста.
        """
        cursor = self.db_connection.cursor()
        cursor.execute(
            "SELECT DISTINCT full_name, birth_date, gender, "
            "strftime('%Y', 'now') - strftime('%Y', birth_date) AS age "
            "FROM employees ORDER BY full_name, birth_date"
        )
        employees = cursor.fetchall()
        for emp in employees:
            print(f"{emp[0]}, {emp[1]}, {emp[2]}, {emp[3]} years")

    def optimize_query(self) -> None:
        """
        Оптимизирует базу данных: создаёт индекс, анализирует статистику, очищает БД.
        """
        cursor = self.db_connection.cursor()

        try:
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_gender_full_name ON employees(gender, full_name)")
            self.db_connection.commit()
            cursor.execute("ANALYZE")
            cursor.execute("PRAGMA optimize")
            cursor.execute("VACUUM")
            self.db_connection.commit()

            self.optimized = True
            print("Optimized database")
        finally:
            cursor.close()
