from mobile_service import create_tables, charge_monthly_fee


def get_calculation_period():
    """Get and validate the number of months for the calculation"""
    while True:
        period = input("Введите период расчета: ")

        try:
            period = int(period)

            if period <= 0:
                print("Ошибка: период расчета должен быть целым числом больше нуля!")
                continue

            return period

        except ValueError:
            print("Ошибка: введите целое число месяцев!")


def main():
    """Run the mobile account billing application"""
    # Первым сообщением в консоли запрашиваем период расчеты
    period = get_calculation_period()

    # После ввода периода создаем таблицы и выполняем списания
    create_tables()
    charge_monthly_fee(period)


if __name__ == "__main__":
    main()