# Employee Service

## Описание
Данное приложение реализует справочник сотрудников с возможностью:
- **Создания таблицы сотрудников.** Таблица содержит поля: "ФИО", "Дата рождения", "Пол" и "Возраст".
- **Добавления записи сотрудника.** Создание объекта класса `Employee` с вводом данных пользователя и сохранением в базу.
- **Вывода всех записей сотрудников.** Вывод уникальных записей, отсортированных по ФИО и дате рождения с расчетом возраста.
- **Автоматического заполнения базы данных.** Генерация 1,000,000 записей со случайными данными и дополнительно 100 записей, где пол фиксирован как "Male" и ФИО начинается с "F".
- **Выполнения запроса по критерию.** Выборка сотрудников с полом "Male" и фамилией, начинающимся с "F" с замером времени выполнения запроса
- **Оптимизации базы данных.** Создание составного индекса для полей `(gender, full_name)` для ускорения запроса. После оптимизации выводится сообщение "Optimized database".

## Структура проекта
- **app.py** – основной модуль, принимающий аргументы командной строки для выполнения различных режимов работы.
- **employee_service.py** – класс `EmployeeService`, реализующий бизнес-логику приложения.
- **models.py** – класс `Employee`, описывающий данные сотрудника и методы для работы с базой данных.
- **database.py** – модуль для получения соединения с базой данных.
- **utils.py** – утилитарный модуль для экспорта результатов замеров времени запросов.
- **config.py** – конфигурационный файл с настройками базы данных.
-**query_performance.txt** - результаты замера времени выполнения до и после оптимизации.

## Режимы работы приложения

1. Создание таблицы сотрудников
    ```bash
    python app.py 1
    
2. Добавление записи сотрудника
    ```bash
    python app.py 2 "Ivanov Petr Sergeevich" 2009-07-12 Male

3. Вывод всех записей сотрудников
    ```bash
    python app.py 3

4. Автоматическое заполнение базы данных
    ```bash
    python app.py 4

5. Выполнение выборки по критерию с замером времени
    ```bash
    python app.py 5

6. Оптимизация базы данных
    ```bash
    python app.py 6


# Оптимизация базы данных SQLite

## Описание
Для ускорения выполнения запросов к базе данных была проведена оптимизация, включающая создание индексов, анализ статистики, а также очистку и изменение базы.

## Выполненные шаги
1. **Создание индекса**
   - Был создан индекс `idx_gender_full_name` на столбцах `gender` и `full_name`:
     ```sql
     CREATE INDEX IF NOT EXISTS idx_gender_full_name ON employees(gender, full_name);
     ```
   - Это улучшает скорость выполнения запросов, содержащих условия фильтрации по `gender` и `full_name`, поскольку индекс позволяет быстрее находить соответствующие строки.

2. **Анализ статистики**
   - Команда `ANALYZE` обновляет статистику SQLite о данных в таблице и индексах, что является наиболее эффективным выполнением поставленной задачи:
     ```sql
     ANALYZE;
     ```

3. **Оптимизация хранилища**
   - Команда `PRAGMA optimize` выполняет дополнительные улучшения базы данных, такие как автоматическое обновление индексов и освобождение свободного пространства.
   - Команда `VACUUM` обновляет базу данных, уменьшая её размер и ускоряя доступ к данным.
     ```sql
     PRAGMA optimize;
     VACUUM;
     ```

## Результаты оптимизации
Были проведены замеры времени выполнения запросов до и после оптимизации:
(можно посмотреть в файле query_performance.txt)

До оптимизации - 0.0041

После оптимизации - 0.0025

В результате оптимизации время выполнения запроса уменьшилось с 4.1 мс до 2.5 мс, что говорит о том, что оптимизация прошла успешно.

Однако в некоторых случаях время выполнения запроса после оптимизации может оказаться больше. 

Возможные причины:
- **Небольшой размер таблицы**: При малом объёме данных использование индекса может не давать значительных преимуществ или даже увеличивать время выполнения.
- **Наличие кэша**: До оптимизации запрос мог выполняться быстрее за счёт уже прогретого кэша, тогда как после очистки и перестроения статистики первый запуск может быть медленнее.
- **Разброс индексов в памяти**: Если структура индекса изменилась, первое выполнение запроса может включать его перестроение.

## Вывод
Применённые техники оптимизации позволили сократить время выполнения запросов за счёт использования индексов, анализа статистики и обновления базы данных.
