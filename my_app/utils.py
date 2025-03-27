import os
from datetime import datetime

def export_calculation(query_time: float) -> None:
    """
    Экспортирует результаты замера времени выполнения запросов в файл.
    """
    file_path = os.path.join(os.path.dirname(__file__), 'query_performance.txt')

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"Performance measurements at {current_time}\n")
        f.write(f"Query time: {query_time:.4f} sec\n")
        f.write("-" * 40 + "\n")

    print(f"Performance calculations exported to {file_path}")


def export_to_file(data: list, filename: str) -> None:
    """
    Экспортирует данные в файл с нумерацией.
    """
    file_path = os.path.join(os.getcwd(), filename)

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            for idx, row in enumerate(data, start=1):
                file.write(f"{idx}. Name: {row[0]}, Birth Date: {row[1]}, Gender: {row[2]}\n")

        print(f"Data has been exported to {file_path}")

    except Exception as e:
        print(f"An error occurred while exporting data: {e}")
