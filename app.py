from flask import Flask, jsonify
import os

from flask import Flask, flash, redirect, render_template, request, session
from login_helper import login_required
from flask_session import Session
import sqlite3

from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.debug = True
Session(app)


# transform to a dict
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# sqlite connection
con = sqlite3.connect('identifier.sqlite', check_same_thread=False, isolation_level=None)
con.row_factory = dict_factory
db = con.cursor()


@app.route('/')
def hello_world():
    if request.method == "GET":
        user = db.execute("select * from users").fetchall()
        print(user[0]["username"])
        return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user ind"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return 0

        # Ensure password was submitted
        elif not request.form.get("password"):
            return 0

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("apologyze.html", message="password is incorrect")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return redirect("/")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/changepass", methods=["GET", "POST"])
@login_required
def changepass():
    if request.method == "POST":

        if not request.form.get("oldpassword"):
            return render_template("apologyze.html", message="must provide the old password")

        oldpassword = request.form.get("oldpassword")
        user = db.execute("select * from users where id = ?", (session["user_id"],)).fetchall()

        if len(user) != 1 or not check_password_hash(user[0]["hash"], oldpassword):
            return render_template("apologyze.html", message="old password incorrect")
        if not request.form.get("newpassword"):
            return render_template("apologyze.html", message="must provide the new password")
        if not request.form.get("passwordrepeat"):
            return render_template("apologyze.html", message="must repeat the new password")
        if request.form.get("newpassword") != request.form.get("passwordrepeat"):
            return render_template("apologyze.html", message="the new password and confirmation password must be equal")

        password = request.form.get("newpassword")
        hash = generate_password_hash(password)
        db.execute("update users set hash = ? where id = ?", (hash, session["user_id"]))

        alert = True
        return render_template("changepass.html", alert=alert)
    else:
        alert = False
        return render_template("changepass.html", alert=alert)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("apologyze.html", message="must submit a username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("apologyze.html", message="must submit a password")

        # Ensure confirmation was submitted
        elif not request.form.get("confirmpassword"):
            return render_template("apologyze.html", message="must provide confirmation")

        # Ensure confirmation and password are equals
        elif request.form.get("confirmpassword") != request.form.get("password"):
            return render_template("apologyze.html", message="the passwords do not match")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchall()

        # Ensure username exists and password is correct
        if len(rows) == 1:
            return render_template("apologyze.html", message="the username already exist")

        # create new user
        username = request.form.get("username")
        password = request.form.get("password")
        hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES(?,?)", (username, hash))

        return redirect("/")
    else:
        return redirect("/")


@app.route("/food", methods=["GET", "POST"])
@login_required
def meals():
    if request.method == "POST":
        return 0
    else:
        foods = db.execute("SELECT * FROM food").fetchall()
        return render_template("food.html", foods=foods)


@app.route("/fooddetail", methods=["GET", "POST"])
@login_required
def fooddetail():
    if request.method == "GET":
        option = request.args.get("food")

        data = db.execute("SELECT * FROM food where name like ?", (option,)).fetchall()
        arrayfood = []
        if data:
            for i in data[0]:
                if i != "id" and i != "name" and i != "calories":
                    a = i.replace("_gr", "")
                    a = a.replace("_", " ")
                    arrayfood.append({'nutrient': a, 'grams': data[0][i]})
        return jsonify(arrayfood)


@app.route("/addfood", methods=["GET", "POST"])
@login_required
def addfood():
    if request.method == "POST":
        name = request.form.get("name")
        if not name:
            return render_template("apologyze.html", message="must provide a name")
        protein = request.form.get("protein")
        message = validate_nutrient(protein, "protein")
        if message:
            return render_template("apologyze.html", message=message)
        carbohydrate = request.form.get("carbohydrate")
        message = validate_nutrient(carbohydrate, "carbohydrate")
        if message:
            return render_template("apologyze.html", message=message)
        fat = request.form.get("fat")
        message = validate_nutrient(fat, "fat")
        if message:
            return render_template("apologyze.html", message=message)
        calcium = request.form.get("calcium")
        message = validate_nutrient(calcium, "calcium")
        if message:
            return render_template("apologyze.html", message=message)
        potassium = request.form.get("potassium")
        message = validate_nutrient(potassium, "potassium")
        if message:
            return render_template("apologyze.html", message=message)
        alcohol = request.form.get("alcohol")
        message = validate_nutrient(alcohol, "alcohol")
        if message:
            return render_template("apologyze.html", message=message)
        iron = request.form.get("iron")
        message = validate_nutrient(iron, "iron")
        if message:
            return render_template("apologyze.html", message=message)
        vitamina = request.form.get("vitamina")
        message = validate_nutrient(vitamina, "vitamina")
        if message:
            return render_template("apologyze.html", message=message)
        vitaminc = request.form.get("vitaminc")
        message = validate_nutrient(vitaminc, "vitaminc")
        if message:
            return render_template("apologyze.html", message=message)
        caffeine = request.form.get("caffeine")
        message = validate_nutrient(caffeine, "caffeine")
        if message:
            return render_template("apologyze.html", message=message)
        calories = request.form.get("calories")
        message = validate_nutrient(calories, "calories")
        if message:
            return render_template("apologyze.html", message=message)

        db.execute(
            "INSERT INTO food (name, protein_gr, total_carbohydrate_gr, total_fat_gr, calcium_gr, potassium_gr,"
            " alcohol_gr, iron_gr, vitamin_a_gr, vitamin_c_gr, caffeine_gr,"
            " calories) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
            (name.replace(".", ","), protein.replace(".", ","), carbohydrate.replace(".", ","), fat.replace(".", ","),
             calcium.replace(".", ","), potassium.replace(".", ","), alcohol.replace(".", ","),
             iron.replace(".", ","), vitamina.replace(".", ","), vitaminc.replace(".", ","), caffeine.replace(".", ","),
             calories.replace(".", ",")))
        return render_template("addfood.html")
    else:
        return render_template("addfood.html")


@app.route("/deletefood", methods=["GET", "POST"])
@login_required
def deletefood():
    if request.method == "POST":
        name = request.form.get("food")
        name_clean = name.replace("+", " ")
        db.execute("DELETE FROM food where name = ?", (name_clean,))
        return redirect("/deletefood")
    else:
        foods = db.execute("SELECT * FROM food").fetchall()
        return render_template("deletefood.html", foods=foods)


@app.route("/deletemeal", methods=["GET", "POST"])
@login_required
def deletemeal():
    if request.method == "POST":
        id = request.form.get("meal")
        if id != '':
            db.execute("DELETE FROM meals where id = ?", (id,))
        return redirect("/deletemeal")
    else:
        meals = db.execute("select a.id as id, b.name as name, a.amount_gr as amount,a.type as type from meals a,"
                           " food b where a.food_id = b.id and user_id = ?", (session["user_id"],)).fetchall()
        return render_template("deletemeal.html", meals=meals)


@app.route("/mealplan", methods=["GET", "POST"])
@login_required
def mealplan():
    if request.method == "POST":
        name = request.form.get("food")
        if not name or name == '':
            return render_template("apologyze.html", message="must provide a food")
        name_clean = name.replace("+", " ")
        type = request.form.get("type")
        if not type or type == '':
            return render_template("apologyze.html", message="must provide the field To")
        amount = request.form.get("amount")
        message = validate_nutrient(amount, "amount")
        if message:
            return render_template("apologyze.html", message=message)

        food_data = db.execute("SELECT * FROM food where name=?", (name_clean,)).fetchall()

        db.execute("INSERT INTO meals (user_id, food_id, type, amount_gr) VALUES(?,?,?,?)", (session["user_id"],
                                                                                             food_data[0]["id"],
                                                                                             type,
                                                                                             amount.replace(".", ",")))
        return redirect("/mealplan")
    else:
        breakfasts = db.execute(
            "select a.name as name, CAST(a.protein_gr as decimal)*(b.amount_gr/100.0) as protein,"
            " CAST(a.total_carbohydrate_gr as decimal)*(b.amount_gr/100.0) as carbohydrate,"
            " CAST(a.total_fat_gr as decimal)*(b.amount_gr/100.0) as fat, CAST(b.amount_gr as decimal) as amount,"
            " CAST(a.calories as decimal)*(b.amount_gr/100.0) as calories from food a,"
            " meals b where a.id = b.food_id and user_id = ? and "
            "type = 'breakfast'", (session["user_id"],)).fetchall()

        lunchs = db.execute(
            "select a.name as name, CAST(a.protein_gr as decimal)*(b.amount_gr/100.0) as protein,"
            " CAST(a.total_carbohydrate_gr as decimal)*(b.amount_gr/100.0) as carbohydrate,"
            " CAST(a.total_fat_gr as decimal)*(b.amount_gr/100.0) as fat, CAST(b.amount_gr as decimal) as amount,"
            " CAST(a.calories as decimal)*(b.amount_gr/100.0) as calories from food a,"
            " meals b where a.id = b.food_id and user_id = ? and "
            "type = 'lunch'", (session["user_id"],)).fetchall()

        dinners = db.execute(
            "select a.name as name, CAST(a.protein_gr as decimal)*(b.amount_gr/100.0) as protein,"
            " CAST(a.total_carbohydrate_gr as decimal)*(b.amount_gr/100.0) as carbohydrate,"
            " CAST(a.total_fat_gr as decimal)*(b.amount_gr/100.0) as fat, CAST(b.amount_gr as decimal) as amount,"
            " CAST(a.calories as decimal)*(b.amount_gr/100.0) as calories from food a,"
            " meals b where a.id = b.food_id and user_id = ? and "
            "type = 'dinner'", (session["user_id"],)).fetchall()

        totals = db.execute("select sum(CAST(a.protein_gr as decimal)*(b.amount_gr/100.0)) as protein,"
                            " sum(CAST(a.total_carbohydrate_gr as decimal)*(b.amount_gr/100.0)) as carbohydrate,"
                            " sum(CAST(a.total_fat_gr as decimal)*(b.amount_gr/100.0)) as fat,"
                            " sum(CAST(a.calories as decimal)*(b.amount_gr/100.0)) as calories from food a,"
                            " meals b where a.id = b.food_id and user_id = ?", (session["user_id"],)).fetchall()

        foods = db.execute("SELECT * FROM food").fetchall()
        return render_template("mealplan.html", foods=foods, breakfasts=breakfasts, dinners=dinners, lunchs=lunchs,
                               totals=totals)


def validate_nutrient(nutrient, name):
    if nutrient == '':
        return "must provide " + name
    char_to_replace = {',': '',
                       '.': ''}
    clean_nutrient = nutrient
    for key, value in char_to_replace.items():
        clean_nutrient = clean_nutrient.replace(key, value)

    if not clean_nutrient.isdigit():
        return "must provide a valid amount of " + name


@app.route("/total", methods=["GET", "POST"])
@login_required
def total():
    if request.method == "POST":
        return redirect("/mealplan")
    else:

        total = db.execute("select sum(CAST(a.protein_gr as decimal)*(b.amount_gr/100.0)) as protein,"
                           " sum(CAST(a.total_carbohydrate_gr as decimal)*(b.amount_gr/100.0)) as carbohydrate,"
                           " sum(CAST(a.total_fat_gr as decimal)*(b.amount_gr/100.0)) as fat from food a,"
                           " meals b where a.id = b.food_id and user_id = ?", (session["user_id"],)).fetchall()
        print(total)
        arr = [{'label': 'protein', 'value': round(total[0]['protein'], 2)},
               {'label': 'carbohydrate', 'value': round(total[0]['carbohydrate'], 2)},
               {'label': 'fat', 'value': round(total[0]['fat'], 2)}]
        return jsonify(arr)


if __name__ == '__main__':
    app.run()
