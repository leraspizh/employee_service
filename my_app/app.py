import sys
from employee_service import EmployeeService

def main() -> None:
    """
    Основная функция для запуска приложения.
    """
    if len(sys.argv) < 2:
        print("Usage: myApp <mode> <params>")
        sys.exit(1)

    mode = sys.argv[1]
    employee_service = EmployeeService()

    if mode == '1':
        employee_service.create_table()
    elif mode == '2' and len(sys.argv) == 5:
        employee_service.create_employee(sys.argv[2], sys.argv[3], sys.argv[4])
    elif mode == '3':
        employee_service.show_all_employees()
    elif mode == '4':
        employee_service.generate_bulk_data(1000000)
    elif mode == '5':
        employee_service.fetch_employees_by_criteria()
    elif mode == '6':
        employee_service.optimize_query()
    else:
        print("Invalid mode or missing parameters.")

if __name__ == '__main__':
    main()
