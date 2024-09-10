import csv
import requests
from datetime import datetime

transactions = []


def add_transaction():
    try:
        amount = float(input("Enter amount: "))
        category = input("Enter category: ")
        date_str = input("Enter date (YYYY-MM-DD): ")
        date = datetime.strptime(date_str, '%Y-%m-%d')
        transactions.append(
            {"amount": amount, "category": category, "date": date})
        print("Transaction added successfully.")
    except ValueError as e:
        print(f"Invalid input: {e}. Please try again.")


def view_balance():
    if not transactions:
        print("No transactions to calculate balance.")
        return

    total = sum(t["amount"] for t in transactions)
    print(f"Total balance: {total}")


def view_history():
    if not transactions:
        print("No transaction history available.")
        return

    for t in transactions:
        print(f"{t['date'].date()} - {t['category']}: {t['amount']}")


def fetch_exchange_rates():
    VALID_CURRENCIES = ['AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT', 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BRL', 'BSD', 'BTC', 'BTN', 'BWP', 'BYN', 'BYR', 'BZD', 'CAD', 'CDF', 'CHF', 'CLF', 'CLP', 'CNY', 'CNH', 'COP', 'CRC', 'CUC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN', 'ETB', 'EUR', 'FJD', 'FKP', 'GBP', 'GEL', 'GGP', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK', 'HTG', 'HUF', 'IDR', 'ILS', 'IMP', 'INR', 'IQD', 'IRR', 'ISK', 'JEP', 'JMD', 'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KMF', 'KPW', 'KRW', 'KWD', 'KYD', 'KZT',
                        'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LTL', 'LVL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRU', 'MUR', 'MVR', 'MWK', 'MXN', 'MYR', 'MZN', 'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLE', 'SLL', 'SOS', 'SRD', 'STD', 'SVC', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TRY', 'TTD', 'TWD', 'TZS', 'UAH', 'UGX', 'USD', 'UYU', 'UZS', 'VEF', 'VES', 'VND', 'VUV', 'WST', 'XAF', 'XAG', 'XAU', 'XCD', 'XDR', 'XOF', 'XPF', 'YER', 'ZAR', 'ZMK', 'ZMW', 'ZWL']

    symbols = input("Enter currencies (comma-separated): ").upper().split(',')
    invalid_symbols = [
        symbol for symbol in symbols if symbol not in VALID_CURRENCIES]

    if invalid_symbols:
        print(f"Invalid currencies: {', '.join(invalid_symbols)}")
        return

    symbols_str = ','.join(symbols)
    url = f"https://api.exchangeratesapi.io/v1/latest?access_key=6ee935c0c1822fd9fde2dc142c5ef193&symbols={
        symbols_str}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        rates = response.json()["rates"]
        print(f"Exchange rates for EUR: {rates}")
        return rates
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rates: {e}")


def generate_csv_report(month):
    try:
        filtered = [t for t in transactions if t["date"].month == month]
        if not filtered:
            print(f"No transactions found for month {month}.")
            return

        with open(f"report_{month}.csv", "w", newline='') as csvfile:
            fieldnames = ["date", "category", "amount"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for t in filtered:
                writer.writerow(
                    {"date": t["date"].date(), "category": t["category"], "amount": t["amount"]})
        print(f"Report for month {month} generated as report_{month}.csv")
    except Exception as e:
        print(f"Error generating CSV report: {e}")


def main():
    while True:
        try:
            print("1. Add Transaction\n2. View Balance\n3. View History\n4. Generate CSV Report\n5. Fetch Exchange Rates\n6. Exit")
            choice = int(input("Choose an option: "))
            if choice == 1:
                add_transaction()
            elif choice == 2:
                view_balance()
            elif choice == 3:
                view_history()
            elif choice == 4:
                month = int(input("Enter month (1-12): "))
                if month < 1 or month > 12:
                    raise ValueError("Month must be between 1 and 12.")
                generate_csv_report(month)
            elif choice == 5:
                fetch_exchange_rates()
            elif choice == 6:
                break
            else:
                print("Invalid choice, please try again.")
        except ValueError as e:
            print(f"Invalid input: {
                  e}. Please enter a number corresponding to the menu options.")


if __name__ == "__main__":
    main()
