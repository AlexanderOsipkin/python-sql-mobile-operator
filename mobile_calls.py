from mobile_calls_service import create_tables, run_daily_calls


def main():
    """Run the mobile calls simulation"""
    # Создаем таблицы и запускаем моделирование звонков на 30 дней
    create_tables()
    run_daily_calls()


if __name__ == "__main__":
    main()