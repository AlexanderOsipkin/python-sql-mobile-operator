# Python SQL Mobile Operator

A console-based mobile operator simulator built with **Python** and **SQLite**. The project contains two independent exercises: monthly mobile tariff billing and daily randomized phone calls with CSV reporting.

## Features

### 1. Monthly Tariff Billing

- Create and populate an SQLite database with mobile users and tariff data.
- Select the calculation period in months through console input.
- Charge each active user the price of their selected tariff once per month.
- Check the account balance before each charge.
- Change a user's `Activity` status to `No` when the balance is insufficient.
- Skip further charges for users whose status is no longer `Yes`.

### 2. Daily Phone Call Simulation

- Create a separate SQLite database with one user and mobile operator prices.
- Simulate one phone call per day for 30 days.
- Randomly select an operator for each call.
- Generate a random call duration between 1 and 10 minutes.
- Calculate the call cost using the operator's per-minute price.
- Check the user's balance before deducting the call cost.
- Save successfully paid calls to a CSV report.

## Tech Stack

- Python 3
- SQLite (`sqlite3`)
- CSV (`csv`)
- Python standard library (`random`, `datetime`)

No external packages are required.

## Project Structure

```text
python-sql-mobile-operator/
├── mobile.py                  # Entry point for monthly tariff billing
├── mobile_service.py          # Database and monthly billing logic
├── mobile_calls.py            # Entry point for daily call simulation
├── mobile_calls_service.py    # Database, call simulation, and CSV reporting
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/AlexanderOsipkin/python-sql-mobile-operator.git
cd python-sql-mobile-operator
```

### 2. Run the monthly tariff billing exercise

```bash
python mobile.py
```

The application asks for the calculation period:

```text
Введите период расчета:
```

Enter a positive integer representing the number of months. The application creates `mobile.db`, initializes the users and tariffs if they do not already exist, and performs the monthly charges.

#### Initial users and tariffs

| User | Initial balance | Tariff | Monthly price |
|---|---:|---|---:|
| User1 | 10000 | VIP | 1000 |
| User2 | 10000 | Premium | 1500 |
| User3 | 10000 | Standard | 500 |

The `mobile_users` table stores user balances and the `Activity` status. The `mobile_tariff` table stores tariff names and prices.

### 3. Run the daily phone call simulation

```bash
python mobile_calls.py
```

This exercise creates `mobile_calls.db` and simulates 30 daily calls for `User1`, whose initial balance is 500. The operator prices are stored in the `mobile_price` table:

| Operator column | Price per minute |
|---|---:|
| `Mts_Mts` | 1 |
| `Mts_Tele2` | 2 |
| `Mts_Yota` | 3 |

For each simulated day, the program randomly selects an operator and a call duration from 1 to 10 minutes. The call cost is calculated as:

```text
Amount = Operator price × Count_min
```

A call is charged only when the account balance is sufficient. Otherwise, the charge is skipped and the balance remains unchanged.

## CSV Report

The daily call simulation creates or updates `report_mobile.csv` in the project working directory.

The report contains the following columns:

| Column | Description |
|---|---|
| `Date` | Simulated call date |
| `Operator` | Selected operator (`Mts_Mts`, `Mts_Tele2`, or `Mts_Yota`) |
| `Count_min` | Call duration in minutes |
| `Amount` | Charged amount |

Only successfully paid calls are added to the report. New records are appended; existing rows are not overwritten.

## Data Persistence and Resetting the Exercises

The databases preserve their data between runs:

- `mobile.db` stores users, tariffs, balances, and activity statuses for the monthly billing exercise.
- `mobile_calls.db` stores the user, operator prices, and the remaining balance for the daily call simulation.
- `report_mobile.csv` accumulates successful calls from the daily call simulation.

To run either exercise again with its original sample data, stop the application and delete the corresponding database file:

- Delete `mobile.db` to reset monthly tariff billing.
- Delete `mobile_calls.db` to reset the daily call simulation.
- Delete `report_mobile.csv` separately if you also want to clear the call report.

The database and CSV files are generated locally and are excluded from version control through `.gitignore`.

## Purpose

This is an educational project for practicing Python fundamentals, SQLite database operations, SQL queries, conditional logic, loops, random data generation, and CSV file handling.
