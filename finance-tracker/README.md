# Command-Line Finance Tracker

#### Video Demo: https://youtu.be/Zbb9Z1TPEng

#### Description:

The Command-Line Finance Tracker is a Python application designed to help users manage their personal finances from the terminal. This project aims to provide a straightforward, yet powerful tool for tracking income and expenses, generating financial reports, and converting currencies based on real-time exchange rates. The simplicity of a command-line interface ensures that users can quickly interact with the tool without needing a graphical user interface.

**Key Features:**

- **Add Transactions:** Users can record their financial transactions, including the amount, category, and date. This allows for a detailed tracking of income and expenditures.
- **View Balance:** The tool calculates and displays the total balance, which is the sum of all recorded transactions. This provides a quick snapshot of the user’s financial status.
- **View Transaction History:** Users can view a detailed list of all transactions, showing the date, category, and amount. This feature is useful for reviewing past financial activities.
- **Fetch Exchange Rates:** Integration with an external API allows users to fetch real-time exchange rates. This is helpful for users who need to convert their balance into different currencies.
- **Generate CSV Reports:** The tool can generate a CSV file summarizing transactions for a selected month. This feature is particularly useful for analyzing spending patterns and preparing financial reports.

### File Descriptions

1. **`finance_tracker.py`**
   - This is the main script of the project. It contains the core functionality of the finance tracker, including:
     - `add_transaction()`: Prompts the user to enter transaction details and adds them to the list of transactions.
     - `view_balance()`: Computes and displays the total balance from the recorded transactions.
     - `view_history()`: Lists all transactions with their date, category, and amount.
     - `fetch_exchange_rates()`: Fetches the latest currency exchange rates using an API and displays them.
     - `generate_csv_report(month)`: Filters transactions by the specified month and generates a CSV report of these transactions.
     - `main()`: The main loop that presents a menu to the user and handles user input.

2. **`README.md`**
   - This file. It provides an overview of the project, detailed descriptions of its features, and information about the implementation and design choices.

### Design Choices and Considerations

1. **Command-Line Interface (CLI):**
   - **Reasoning:** A CLI was chosen for simplicity and ease of use. It allows users to interact with the application without the need for a graphical user interface, making it more accessible and faster to implement.
   - **Benefits:** The CLI is lightweight and runs on any system with Python installed, making it ideal for quick, efficient financial tracking.

2. **Data Storage:**
   - **Choice:** Transactions are stored in memory using a list of dictionaries.
   - **Reasoning:** For simplicity, data is not stored persistently in a database or file system within this version. However, for future improvements, adding file-based or database storage could be considered.

3. **API Integration:**
   - **API Used:** The project uses the Exchange Rates API to fetch real-time currency exchange rates.
   - **Reasoning:** This API provides a straightforward way to access exchange rates with minimal setup. The `requests` library in Python is used for making HTTP requests to this API.
   - **Considerations:** Error handling is included to manage cases where the API request fails or returns unexpected results.

4. **CSV Report Generation:**
   - **Library Used:** The `csv` module is used to create CSV files for reporting.
   - **Reasoning:** The CSV format is widely used and compatible with many tools and applications, making it a good choice for exporting financial data. The `csv` module provides a simple way to write structured data to a file.

5. **Error Handling:**
   - **Implementation:** Basic error handling is included to manage invalid input and API errors.
   - **Reasoning:** Ensuring that the program handles incorrect input gracefully improves user experience and robustness. For instance, the program checks for valid date formats and numerical inputs.

### Future Improvements

1. **Persistent Storage:**
   - Implementing file-based or database storage would allow users to save and load transactions between sessions, enhancing the tool’s utility.

2. **User Authentication:**
   - Adding user authentication could provide a more secure and personalized experience, especially if multiple users share the application.

3. **Enhanced Reporting:**
   - Additional features such as monthly or yearly summaries, charts, and graphical reports could provide deeper insights into financial data.

4. **GUI Integration:**
   - Although the CLI is functional, a graphical user interface (GUI) could make the application more accessible to users who prefer visual interaction.
