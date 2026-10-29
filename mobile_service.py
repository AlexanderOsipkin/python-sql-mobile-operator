import sqlite3


DB_NAME = "mobile.db"
DB_USERS = "mobile_users"
DB_TARIFF = "mobile_tariff"


def create_tables():
    """Create the required tables and insert initial data if they do not already exist"""
    with sqlite3.connect(DB_NAME) as db:
        cur = db.cursor()

        # Создаем таблицу пользователей мобильной связи.
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {DB_USERS} (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            User_name TEXT NOT NULL UNIQUE,
            Balance INTEGER NOT NULL,
            Mobile_tariff_ref INTEGER NOT NULL,
            Activity TEXT NOT NULL
        );""")

        # Создаем таблицу мобильных тарифов.
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {DB_TARIFF} (
            TariffID INTEGER PRIMARY KEY,
            Tariff TEXT NOT NULL,
            Price INTEGER NOT NULL
        );""")

        print(f"Таблицы {DB_USERS} и {DB_TARIFF} созданы или уже существуют")

        # Добавляем тарифы, повторные записи не дублируются
        cur.executemany(
            f"""INSERT OR IGNORE INTO {DB_TARIFF} (TariffID, Tariff, Price)
            VALUES (?, ?, ?);""",
            [
                (1, "Standard", 500),
                (2, "VIP", 1000),
                (3, "Premium", 1500),
            ],
        )

        # Добавляем пользователей, повторные записи не дублируются
        cur.executemany(
            f"""INSERT OR IGNORE INTO {DB_USERS}
            (User_name, Balance, Mobile_tariff_ref, Activity)
            VALUES (?, ?, ?, ?);""",
            [
                ("User1", 10000, 2, "Yes"),
                ("User2", 10000, 3, "Yes"),
                ("User3", 10000, 1, "Yes"),
            ],
        )

        db.commit()
        print("Начальные данные пользователей и тарифов добавлены или уже существуют")


def charge_monthly_fee(period):
    """Charge active users their monthly tariff fee for the requested period"""
    with sqlite3.connect(DB_NAME) as db:
        cur = db.cursor()

        # Выполняем списание последовательно за каждый месяц
        for month in range(1, period + 1):
            cur.execute("""SELECT mobile_users.UserID,
                                  mobile_users.User_name,
                                  mobile_users.Balance,
                                  mobile_tariff.Price
                           FROM mobile_users
                           JOIN mobile_tariff
                             ON mobile_users.Mobile_tariff_ref = mobile_tariff.TariffID
                           WHERE mobile_users.Activity = 'Yes'
                           ORDER BY mobile_users.UserID;""")

            users = cur.fetchall()

            # Если активных пользователей не осталось, завершаем расчет
            if not users:
                print(f"За месяц №{month} нет активных пользователей для списания.")
                break

            for user in users:
                user_id, user_name, balance, price = user

                # Проверяем баланс перед списанием, чтобы он не стал отрицательным
                if balance >= price:
                    new_balance = balance - price

                    cur.execute(
                        f"UPDATE {DB_USERS} SET Balance = ? WHERE UserID = ?;",
                        (new_balance, user_id),
                    )

                    print(f"{user_name} снятие денежных средств {price} за месяц №{month}")

                else:
                    # При недостатке средств отключаем пользователя от следующих списаний
                    cur.execute(
                        f"UPDATE {DB_USERS} SET Activity = 'No' WHERE UserID = ?;",
                        (user_id,),
                    )

                    print(f"{user_name} недостаточно средств на балансе! Баланс: {balance}, стоимость тарифа: {price}. Статус Activity изменен")

            # Сохраняем результаты для каждого месяца списания
            db.commit()

    print("Расчет завершен")