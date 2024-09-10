import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    rows = db.execute("""
        SELECT symbol, SUM(shares) as total_shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING total_shares > 0
    """, user_id)

    portfolio = []

    total_stocks_value = 0

    for row in rows:
        symbol = row["symbol"]
        shares = row["total_shares"]

        stock = lookup(symbol)
        if stock:
            current_price = stock["price"]
            total_value = current_price * shares
            total_stocks_value += total_value

            portfolio.append({
                "symbol": symbol,
                "shares": shares,
                "price": usd(current_price),
                "total": usd(total_value)
            })

    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[
        0]["cash"]

    grand_total = cash + total_stocks_value

    return render_template("index.html", portfolio=portfolio, cash=usd(cash), grand_total=usd(grand_total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide stock symbol", 400)

        stock = lookup(symbol)
        print(stock)
        if stock is None:
            return apology("invalid stock symbol", 400)

        try:
            shares = int(shares)
            if shares <= 0:
                return apology("must provide a positive number of shares", 400)
        except ValueError:
            return apology("shares must be a positive integer", 400)

        user_id = session["user_id"]
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[
            0]["cash"]

        price = stock["price"]
        total_cost = price * shares

        if total_cost > user_cash:
            return apology("you do not have enough cash", 403)

        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?",
                   total_cost, user_id)

        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price, total, transacted) VALUES (?, ?, ?, ?, ?, ?)",
            user_id, symbol, shares, price, total_cost, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]

    transactions = db.execute("""
        SELECT symbol, shares, price, transacted
        FROM transactions
        WHERE user_id = ?
        ORDER BY transacted DESC
    """, user_id)

    for transaction in transactions:
        if transaction["shares"] > 0:
            transaction["type"] = "Buy"
        else:
            transaction["type"] = "Sell"
            transaction["shares"] = abs(transaction["shares"])

        transaction["price"] = usd(transaction["price"])
        transaction["transacted"] = transaction["transacted"]

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide stock symbol", 400)

        stock = lookup(symbol)
        if stock is None:
            return apology("invalid stock symbol", 400)

        return render_template("quoted.html", stock=stock)

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            return apology("must provide username", 400)

        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not password or not confirmation:
            return apology("must provide password and confirmation", 400)

        if password != confirmation:
            return apology("passwords must match", 400)

        hashed_password = generate_password_hash(password)

        try:
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                username, hashed_password
            )
        except ValueError:
            return apology("username already exists", 400)

        return redirect("/login")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must select a stock")
        if not shares.isdigit() or int(shares) <= 0:
            return apology("shares must be a positive integer")

        shares = int(shares)

        rows = db.execute("""
            SELECT SUM(shares) as total_shares
            FROM transactions
            WHERE user_id = ? AND symbol = ?
            GROUP BY symbol
        """, user_id, symbol)

        if len(rows) != 1 or rows[0]["total_shares"] < shares:
            return apology("not enough shares")

        stock = lookup(symbol)
        if stock is None:
            return apology("invalid stock symbol")

        current_price = stock["price"]
        total_value = current_price * shares

        db.execute("""
            INSERT INTO transactions (user_id, symbol, shares, price, total, transacted)
            VALUES (?, ?, ?, ?, ?, ?)
        """, user_id, symbol, -shares, current_price, total_value, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?",
                   total_value, user_id)

        return redirect("/")

    else:
        stocks = db.execute("""
            SELECT symbol
            FROM transactions
            WHERE user_id = ?
            GROUP BY symbol
            HAVING SUM(shares) > 0
        """, user_id)

        return render_template("sell.html", stocks=stocks)


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Allow user to add additional cash to their account"""
    if request.method == "POST":
        cash = request.form.get("cash")

        if not cash or not cash.isdigit() or int(cash) <= 0:
            return apology("must provide a valid amount of cash", 403)

        cash = int(cash)

        user_id = session["user_id"]
        current_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        db.execute("UPDATE users SET cash = ? WHERE id = ?", current_cash + cash, user_id)

        return redirect("/")

    else:
        return render_template("add_cash.html")
