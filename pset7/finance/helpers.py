import csv
import os
import urllib.request

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Reject symbol if it starts with caret
    if symbol.startswith("^"):
        return None

    # Reject symbol if it contains comma
    if "," in symbol:
        return None

    # Query Alpha Vantage for quote
    # https://www.alphavantage.co/documentation/
    try:

        # GET CSV
        url = f"https://www.alphavantage.co/query?apikey={os.getenv('API_KEY')}&datatype=csv&function=TIME_SERIES_INTRADAY&interval=1min&symbol={symbol}"
        webpage = urllib.request.urlopen(url)

        # Parse CSV
        datareader = csv.reader(webpage.read().decode("utf-8").splitlines())

        # Ignore first row
        next(datareader)

        # Parse second row
        row = next(datareader)

        # Ensure stock exists
        try:
            price = float(row[4])
        except:
            return None

        # Return stock's name (as a str), price (as a float), and (uppercased) symbol (as a str)
        return {
            "price": price,
            "symbol": symbol.upper()
        }

    except:
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

def calculate(totalList):
    total = 0.0
    for i in totalList:

        existingTotal1 = i["total"].split("$")
        if "," in existingTotal1[1]:
            existingTotal2 = existingTotal1[1].split(",")
            existingTotal4 = existingTotal2[0]+existingTotal2[1]
        else:
            existingTotal4 = existingTotal1[1]

        total = total + float(existingTotal4)

    return float(total)

def percentage(a,b):
    priceA = a.split("$")
    if "," in priceA[1]:
        priceA1 = priceA[1].split(",")
        priceA2 = priceA1[0]+priceA1[1]
    else:
        priceA2 = priceA[1]

    priceB = b.split("$")
    if "," in priceB[1]:
        priceB1 = priceB[1].split(",")
        priceB2 = priceB1[0]+priceB1[1]
    else:
        priceB2 = priceB[1]

    #a is userStatus price
    #b is stockmarket price

    #100 ja 110

    return str(round(float(priceB2)*100/float(priceA2)-100,2))+"%"

