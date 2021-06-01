from flask import Flask, request, g, session, flash, jsonify
from setup_db import *
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.debug = True
app.secret_key = 'some_secret'
app.config.update(
    SESSION_COOKIE_SAMESITE='Strict',
)

# Get database
def get_db():
    if not hasattr(g, "_database"):
        print("create connection")
        g._database = sqlite3.connect("database.db")
    return g._database

# Close the database at the end of the request
@app.teardown_appcontext
def teardown_db(error):
    db = getattr(g, '_database', None)
    if db is not None:
        print("close connection")
        db.close()

# Checks if username-password combination is valid
def valid_login(username, password):
    # user password data is stored in a database
    conn = get_db()

    hash = get_hash_for_login(conn, username)
    # the generate a password hash use the line below:
    # generate_password_hash("rawPassword")
    if hash != None:
        return check_password_hash(hash, password)
    return False

def validate_userinput(userinput, key):
    # List with special characters that are not allowed in input field
    print(userinput)
    avoid = ['#', '$', '%', '=', '{', '}', '[', ']', '\\', '*', '^', '¨', '~', '§', '>', '<']
    if key == "bid":
        return ""
    if userinput == "static/img/":
        return "Skriv inn filnavn"
    if userinput == None:
        return ""
    if key == "Brukernavn":
        userinput = userinput.strip()
    for char in avoid:
        if char in userinput:
            return key + " tillatter ikke spessialtegn, prøv igjen!"
    if key == "Passord":
        if len(userinput) < 8:
            return key + " må ha minst 8 tegn!"
    if len(userinput) < 3:
        return key + " må ha minst 3 tegn!"
    return "Ok"

# Check if there is a logged in user
@app.route("/userdata")
def userdata():
    if session.get("username", None):
        username = session.get("username")
        user = get_user_by_name(get_db(),username)
        return {"userid": user["userid"], "username": user["username"], "role": user["role"]}
    return jsonify("")


@app.route("/login", methods=["GET", "POST"])
def login():
    # if the form was submitted (otherwise we just display form)
    if request.method == "POST":  
        user_form = request.get_json()
        username = user_form["username"]
        password = user_form["password"]
        if valid_login(username, password):
            conn = get_db()
            user = get_user_by_name(conn,username)
            session["username"] = user["username"]
            print(session["username"])
            session["role"] = user["role"]
            return {"userid": user["userid"], "username": user["username"], "role": user["role"] }
        else:
            return jsonify("Feil brukernavn eller passord!")
    return {}

@app.route("/register", methods=["POST"])
def register():
    user_form = request.get_json()
    username = user_form["Brukernavn"]
    password = user_form["Passord"]
    valPassword = user_form["SjekkPassord"]

    if password != valPassword:
        return jsonify("Passordene må være like!")

    # Sjekker brukerinput ved registrering
    for key in user_form:
        text = validate_userinput(user_form[key], key)
        if text != "Ok":
            return jsonify(text)

    hash = generate_password_hash(password)
    
    conn = get_db()
    id = add_user(conn, username, hash)
    if id == -1:
        return jsonify("Brukernavnet er allerede tatt!")

    name = user_form["Bedriftnavn"]
    phone = user_form["Telefon"]
    address = user_form["Adresse"]
    mail = user_form["Mail"]
    filename = user_form["Filnavn"]

    add_company(conn, name, phone, address, mail, filename, id)

    session["username"] = username
    user = get_user_by_name(conn,username)
    return jsonify("Sucess")

@app.route("/bedrift")
def get_bedrift():
    conn = get_db()
    username = session["username"]
    user = get_user_by_name(conn,username)
    company = get_company(conn, user["userid"])
    return company

@app.route("/styret")
def get_styret():
    conn = get_db()
    username = session["username"]
    user = get_user_by_name(conn,username)
    styret = get_mld(conn, user["userid"])
    return styret

@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("role", None)
    return ""

@app.route("/innlegg", methods=["GET", "POST"])
def innlegg():
    if request.method == "POST":
        conn = get_db()
        username = session["username"]
        user = get_user_by_name(conn,username)
        innlegg = request.get_json()
        for key in innlegg:
            text = validate_userinput(innlegg[key], key)
            if text != "Ok" and text != "":
                return jsonify(text)
        id = make_post(conn, innlegg["Beskrivelse"], innlegg["Dato"], user["userid"], innlegg["type"], innlegg["Sted"], innlegg["Lenke"], innlegg["Tittel"])
    return jsonify("Success")

@app.route("/post", methods=["GET"])
def getInnlegg():
    conn = get_db()
    innlegg = get_post(conn)
    for post in innlegg:
        if post["type"] == "innlegg":
            post["userid"] = get_mld(conn, post["userid"])
            print(post["userid"]["firstname"])
        else:
            post["userid"] = get_company(conn, post["userid"])
            print(post["userid"]["name"])
    return jsonify(innlegg)

@app.route("/delete", methods=["GET"])
def delete():
    conn = get_db()
    post_id = request.args.get("post_id", "")
    message = delete_post(conn, post_id)
    return getInnlegg()

@app.route("/avtaler", methods=["GET"])
def getAvtaler():
    conn = get_db()
    bid = request.args.get("bid", "")
    print(bid)
    return jsonify(get_deals_by_bid(conn, bid))

@app.route("/alleAvtaler")
def getAllAvtaler():
    conn = get_db()
    avtaler = get_deals(conn)
    for deal in avtaler:
        deal["bid"] = get_company_by_bid(conn, deal["bid"])
    return jsonify(avtaler)

@app.route("/admin")
def adminonly():
    if not session.get("role",None) == "admin":
        return jsonify(False)
    return get_styret()

# Route to edit company info.
@app.route("/editInfo", methods=["POST"])
def editCompInfo():
    conn = get_db()
    edit_form = request.get_json()
    for key in edit_form:
        text = validate_userinput(str(edit_form[key]), key)
        if text != "Ok" and text != "":
            print("hei")
            return jsonify(text)
    bid = edit_form["bid"]
    name = edit_form["Navn"]
    phone_numb = edit_form["Telefon"]
    mail = edit_form["Mail"]
    address = edit_form["Adresse"]
    filename = edit_form["Filnavn"]
    edit_company_info(conn, bid, name, phone_numb, mail, address, filename)

    return jsonify("Sucess")

@app.route("/")
def index():
    return app.send_static_file("index.html")


if __name__ == "__main__":
    app.run()
