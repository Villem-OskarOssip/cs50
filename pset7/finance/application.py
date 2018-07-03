import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, calculate, percentage

# Ensure environment variable is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

# Configure application
app = Flask(__name__)


m1 = ""
m2 = ""

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():

    totalList = db.execute("SELECT total FROM userStatus WHERE id = :id", id=session["user_id"])

    total = calculate(totalList)

    userStatus = db.execute("SELECT * from userStatus WHERE id=:id", id=session["user_id"])

    cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])

    user = db.execute("SELECT username FROM users WHERE id=:id", id=session["user_id"])

    stockmarket = []

    for s in userStatus:
        x = lookup(s["symbol"])
        stockmarket.append(x)

    print(stockmarket)

    for s in stockmarket:
        for u in userStatus:
            if s is None:
                break
            elif u["symbol"] == s["symbol"]:
                u["percentage"] = percentage(u["price"],usd(s["price"]))
                u["marketprice"] = usd(s["price"])


    global m1;
    global m1;
    message11 = m1[:]
    message22 = m2[:]
    m1 = ""
    m1 = ""

    return render_template("index.html",username=(user[0]["username"]), stocks=userStatus, \
    cash=usd(float(cash[0]["cash"])), total=usd(total+float(cash[0]["cash"])), \
    message1= message11, message2=message22)



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":

        name = request.form.get("name")
        shares = request.form.get("shares")
        id=session["user_id"]

        if not name:
            return apology("Must provide symbol", 403)

        if not shares:
            return apology("Must provide number of shares", 403)

        try:
            sharesInt = int(shares)
        except:
            return apology("Must provide number not string", 403)

        if (sharesInt <= 0):
            return apology("Number of positive number", 403)

        balance = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        stock = lookup(request.form.get("name"))

        if not stock:
            return apology("Invalid Symbol")

        if float(balance[0]["cash"]) < (sharesInt * stock["price"]):
            return apology("Not enough money to buy stocks", 403)


        db.execute("INSERT INTO history (id, action, symbol, shares, price) VALUES(:id, :action, :symbol, :shares, :price)", \
                    id=session["user_id"], action="BUY", symbol=stock["symbol"], \
                    shares=sharesInt, price=usd(stock["price"]))


        db.execute("UPDATE users SET cash=cash- :transaction WHERE id = :id", \
                    id=session["user_id"], transaction=str(sharesInt * stock["price"]))


        existingShares = db.execute("SELECT shares FROM userStatus WHERE id = :id AND symbol=:symbol", \
                           id=session["user_id"], symbol=stock["symbol"])


        if not existingShares:
            db.execute("INSERT INTO userStatus (id, symbol, shares, price, total) VALUES(:id, :symbol, :shares, :price, :total)", \
                        id=session["user_id"], symbol=stock["symbol"], \
                        shares=sharesInt, price=usd(stock["price"]), \
                        total=usd(sharesInt * stock["price"]))

        else:
            existingTotalUSD = db.execute("SELECT total FROM userStatus WHERE id = :id", \
                           id=session["user_id"])

            existingTotalClean = calculate(existingTotalUSD)
            total1= usd(existingTotalClean+float(sharesInt * stock["price"]))

            db.execute("UPDATE userStatus SET shares=:shares, total=:total WHERE id=:id AND symbol=:symbol", \
                        shares=(sharesInt + existingShares[0]["shares"]),\
                        id=session["user_id"], \
                        symbol=stock["symbol"], \
                        total=total1)
        global m1;
        global m2;
        m1 = "Bought! "
        m2 = str(stock["symbol"]) +" for "+ str(usd(stock["price"]))+" in total of " + str(usd(sharesInt * stock["price"]))
        return redirect("/")

    else:
        return render_template("buy.html")

@app.route("/money", methods=["GET", "POST"])
@login_required
def money():
    if request.method == "POST":
        global m1, m2

        money = request.form.get("addMoney")
        takeMoney = request.form.get("takeMoney")

        if takeMoney:
            try:
                moneyFloat = float(takeMoney)
            except:
                return apology("Must provide number not string", 403)

            if (moneyFloat <= 0):
                return apology("Must be positive number", 403)

            balance = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
            newBalance = float(balance[0]["cash"]) - moneyFloat
            if newBalance <=0:
                return apology("You don't have enough money", 403)


            db.execute("INSERT INTO history (id, action, price) VALUES(:id, :action, :price)", \
                        id=session["user_id"], action="CASH TAKEN", price=usd(moneyFloat))


            db.execute("UPDATE users SET cash=:newBalance WHERE id = :id", \
                        id=session["user_id"], newBalance=newBalance)

            m1 = "Cash taken! "
            m2 = str(usd(moneyFloat))
            return redirect("/")

        else:

            if not money:
                return apology("Must provide money", 403)

            try:
                moneyFloat = float(money)
            except:
                return apology("Must provide number not string", 403)

            if (moneyFloat <= 0):
                return apology("Must be positive number", 403)

            balance = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
            newBalance = moneyFloat + float(balance[0]["cash"])


            db.execute("INSERT INTO history (id, action, price) VALUES(:id, :action, :price)", \
                        id=session["user_id"], action="CASH ADDED", price=usd(moneyFloat))


            db.execute("UPDATE users SET cash=:newBalance WHERE id = :id", \
                        id=session["user_id"], newBalance=newBalance)

            m1 = "Cash added! "
            m2 = str(usd(moneyFloat))
            return redirect("/")

    else:
        return render_template("money.html")


@app.route("/history")
@login_required
def history():

    allHistory = db.execute("SELECT * from history WHERE id=:id", id=session["user_id"])
    print(allHistory)

    return render_template("history.html", history=allHistory)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    session.clear()

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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
        fullStock = lookup(request.form.get("name"))

        if not fullStock:
            return apology("Invalid Symbol")

        return render_template("quoted.html", stock=fullStock)

    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        elif not request.form.get("confirmation"):
            return apology("must provide confirm password", 403)

        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("passwords do not match", 403)

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        if len(rows) == 1:
            return apology("This username has already been taken. Try again!", 403)
        else:
            username = request.form.get("username")
            passwordHash = generate_password_hash(request.form.get("password"))

            db.execute("INSERT INTO users (username, hash) VALUES (:username, :passwordHash)", username=username, passwordHash=passwordHash)

        global m1, m2
        m1 = "Success!"
        m2 = " Account registered!"
        return redirect("/")


    else:
        return render_template("register.html")

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():

    if request.method == "POST":

        if not request.form.get("oldPassword"):
            return apology("must provide old password", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        elif not request.form.get("confirmation"):
            return apology("must provide confirm password", 403)

        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("passwords do not match", 403)

        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("passwords do not match", 403)


        password = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])


        if not check_password_hash(password[0]["hash"], request.form.get("oldPassword")):
            return apology("invalid password", 403)


        else:
            passwordHash = generate_password_hash(request.form.get("confirmation"))

            db.execute("INSERT INTO users (hash) VALUES (:passwordHash)", passwordHash=passwordHash)
        global m1, m2
        m1 = "Password changed"
        m2 = ""

        return redirect("/")

    else:
        return render_template("settings.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    if request.method == "POST":

        try:
            shares = int(request.form.get("shares"))
            if shares < 0:
                return apology("Shares must be positive integer",403)
        except:
            return apology("Must provide positive integer",403)


        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("Invalid Symbol",403)


        availableShares = db.execute("SELECT shares FROM userStatus WHERE id = :id AND symbol=:symbol", \
                                 id=session["user_id"], symbol=stock["symbol"])

        if shares > int(availableShares[0]["shares"]):
            return apology("Not enough shares to sell", 403)

        db.execute("INSERT INTO history (id, action, symbol, shares, price) VALUES(:id, :action, :symbol, :shares, :price)", \
                    id=session["user_id"], action="SELL", symbol=stock["symbol"], shares=shares, \
                    price=usd(stock["price"]), )

        db.execute("UPDATE users SET cash = cash + :sellValue WHERE id = :id", \
                    sellValue= (stock["price"] * float(shares)), id=session["user_id"] )

        totalShares = availableShares[0]["shares"] - shares

        availabletotal = db.execute("SELECT total FROM userStatus WHERE id = :id AND symbol=:symbol", \
                                 id=session["user_id"], symbol=stock["symbol"])

        existingTotalClean = calculate(availabletotal)

        if totalShares > 0:
            db.execute("UPDATE userStatus SET shares=:shares, total=:value  WHERE id=:id AND symbol=:symbol", \
                    shares=totalShares, id=session["user_id"], symbol=stock["symbol"], \
                    value=usd(existingTotalClean - (int(shares) * stock["price"])))
        else:
            db.execute("DELETE FROM userStatus WHERE id=:id AND symbol=:symbol", \
                        id=session["user_id"], symbol=stock["symbol"])


        global m1, m2
        m1 = "Sold! "
        m2 = str(stock["symbol"]) +" for "+ str(usd(stock["price"])) +" in total of " + str(usd(shares * stock["price"]))
        return redirect("/")
    else:

        userStatus = db.execute("SELECT * from userStatus WHERE id=:id", id=session["user_id"])
        return render_template("sell.html", stocks = userStatus)

def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
