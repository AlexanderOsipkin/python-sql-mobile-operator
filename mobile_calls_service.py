import csv
import random
import sqlite3
from datetime import date, timedelta


DB_NAME = "mobile_calls.db"
DB_USERS = "mobile_users"
DB_PRICE = "mobile_price"
REPORT_NAME = "report_mobile.csv"
DAYS_IN_MONTH = 30


def create_tables():
    """Create the database tables and insert the initial data if it does not exist"""
    with sqlite3.connect(DB_NAME) as db:
        cur = db.cursor()

        # Создаем таблицу пользователей мобильной связи.
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {DB_USERS} (
            UserID INTEGER PRIMARY KEY,
            User TEXT NOT NULL,
            Balance INTEGER NOT NULL
        );""")

        # Создаем таблицу стоимости звонков мобильных операторов.
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {DB_PRICE} (
            PriceID INTEGER PRIMARY KEY,
            Mts_Mts INTEGER NOT NULL,
            Mts_Tele2 INTEGER NOT NULL,
            Mts_Yota INTEGER NOT NULL
        );""")

        print(f"Таблицы {DB_USERS} и {DB_PRICE} созданы или уже существуют")

        # Добавляем пользователя из условия задания, повторные записи не дублируются.
        cur.execute(
            f"""INSERT OR IGNORE INTO {DB_USERS} (UserID, User, Balance)
            VALUES (?, ?, ?);""",
            (1, "User1", 500)
        )

        # Добавляем стоимость минуты звонка для операторов, повторные записи не дублируются.
        cur.execute(
            f"""INSERT OR IGNORE INTO {DB_PRICE}
            (PriceID, Mts_Mts, Mts_Tele2, Mts_Yota)
            VALUES (?, ?, ?, ?);""",
            (1, 1, 2, 3)
        )

        db.commit()
        print("Начальные данные пользователя и стоимости звонков добавлены или уже существуют")


def report_operation(now_date, operator, count_min, amount):
    """Append a successfully paid call to the CSV report"""
    try:
        # Открываем отчет для добавления новых записей, не удаляя старые.
        with open(REPORT_NAME, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # Добавляем заголовки только при создании пустого файла.
            if file.tell() == 0:
                writer.writerow(["Date", "Operator", "Count_min", "Amount"])

            # Записываем дату, оператора, длительность звонка и сумму списания.
            writer.writerow([now_date, operator, count_min, amount])

        print(f"Данные внесены в отчет {REPORT_NAME}.")
        return True

    except OSError as error:
        print(f"Ошибка записи в отчет {REPORT_NAME}: {error}")
        return False


def run_daily_calls():
    """Simulate one randomly selected phone call per day for 30 days"""
    with sqlite3.connect(DB_NAME) as db:
        cur = db.cursor()

        # Получаем пользователя из таблицы mobile_users.
        cur.execute(
            f"SELECT UserID, User, Balance FROM {DB_USERS} WHERE UserID = ?;",
            (1,)
        )
        user = cur.fetchone()

        if user is None:
            print("Ошибка: пользователь User1 не найден в базе данных.")
            return

        # Получаем стоимость минуты звонка для каждого оператора из таблицы mobile_price.
        cur.execute(
            f"""SELECT Mts_Mts, Mts_Tele2, Mts_Yota
            FROM {DB_PRICE}
            WHERE PriceID = ?;""",
            (1,)
        )
        prices = cur.fetchone()

        if prices is None:
            print("Ошибка: данные операторов не найдены в таблице mobile_price.")
            return

        # Формируем список операторов и стоимости одной минуты звонка.
        operators = [
            ("Mts_Mts", prices[0]),
            ("Mts_Tele2", prices[1]),
            ("Mts_Yota", prices[2])
        ]

        # Используем текущую дату как дату первого звонка.
        start_date = date.today()
        user_id, user_name, balance = user

        print(f"Начинаем моделирование звонков на {DAYS_IN_MONTH} дней.")

        # Выполняем 30 ежедневных итераций.
        for day in range(1, DAYS_IN_MONTH + 1):

            # Случайно выбираем оператора и длительность звонка от 1 до 10 минут.
            operator, price_per_minute = random.choice(operators)
            count_min = random.randint(1, 10)
            amount = price_per_minute * count_min
            now_date = (start_date + timedelta(days=day - 1)).strftime("%Y-%m-%d")

            print(f"День №{day}: {now_date}")
            print(f"{user_name}: оператор {operator}, длительность звонка {count_min} мин., стоимость {amount}.")

            # Проверяем баланс перед списанием, чтобы он не стал отрицательным.
            if balance >= amount:
                new_balance = balance - amount

                # Списываем деньги с баланса пользователя.
                cur.execute(
                    f"UPDATE {DB_USERS} SET Balance = ? WHERE UserID = ?;",
                    (new_balance, user_id)
                )
                db.commit()

                print(f"{user_name}: успешно списано {amount}. Остаток на балансе: {new_balance}.")

                # Добавляем в CSV только успешно оплаченный звонок.
                report_operation(now_date, operator, count_min, amount)

                # Обновляем баланс для следующей итерации.
                balance = new_balance

            else:
                # При недостатке средств не выполняем списание и не допускаем отрицательный баланс.
                print(f"{user_name}: недостаточно средств на балансе. Баланс: {balance}, стоимость звонка: {amount}. Списание не выполнено.")

        print(f"Моделирование завершено. Итоговый баланс {user_name}: {balance}")