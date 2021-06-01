from flask import Flask, request, session, jsonify
from setup_db import *
from func import *
from werkzeug.security import generate_password_hash, check_password_hash
from io import BytesIO
from PIL import Image
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.debug = True
app.secret_key = 'some_secret'
app.config.update(
    SESSION_COOKIE_SAMESITE='Strict',
)
UPLOAD_FOLDER = '/path/to/the/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Close the database at the end of the request
@app.teardown_appcontext
def teardown_db(error):
    db = getattr(g, '_database', None)
    if db is not None:
        print("close connection")
        db.close()

# Check if there is a loggedin user
@app.route("/userdata", methods=["GET"])
def userdata():
    if session.get("username", None):
        username = session.get("username")
        user = get_user_by_name(get_db(),username)
        return user
    return jsonify("")

@app.route("/logout", methods=["GET"])
def logout():
    session.pop("username", None)
    session.pop("role", None)
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
            user = get_user_by_name(conn, username)
            session["username"] = user["username"]
            session["role"] = user["role"]
            return jsonify(user)
        else:
            return jsonify("Feil brukernavn eller passord!")
    return jsonify("")

# Sjekker om innlogget bruker er admin - returnerer styremedlem
@app.route("/admin", methods=["GET"])
def adminonly():
    conn = get_db()
    if not session.get("role", None) == "admin":
        return jsonify(False)
    username = session["username"]
    user = get_user_by_name(conn,username)
    medlem = get_mld(conn, user["userid"])
    return jsonify(medlem)


@app.route("/register", methods=["POST"])
def register():
    conn = get_db()
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
    id = add_user(conn, username, hash)
    if id == -1:
        return jsonify("Brukernavnet er allerede tatt!")

    # Legger til bedriften i bedrift-tabell
    add_company(conn, user_form["Bedriftnavn"], user_form["Telefon"], user_form["Adresse"], user_form["Mail"], id)

    return jsonify("Sucess")

# Henter logget inn bedrift fra userid
@app.route("/bedrift", methods=["GET"])
def get_bedrift():
    conn = get_db()
    username = session["username"]
    user = get_user_by_name(conn,username)
    company = get_company(conn, user["userid"])
    img = get_img_from_bid(conn, company["bid"])
    if img["filename"] != None:
        company["filename"] = img["filename"]
    return jsonify(company)


# ---- INNLEGG ----
# Lager innlegg, sjekker brukerinput
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

# Henter innlegg
# Legger til dict for userid med styremedlem for innlegg og userid med bedriftinfo for stillingsannonse
@app.route("/post", methods=["GET"])
def getInnlegg():
    conn = get_db()
    innlegg = get_post(conn)
    innleggType(conn, innlegg)
    return jsonify(innlegg)

# Sletter innlegg eller stillingsannonser, returnerer innleggene
@app.route("/delete", methods=["GET"])
def delete():
    conn = get_db()
    post_id = request.args.get("post_id", "")
    message = delete_post(conn, post_id)
    innlegg = get_post(conn)
    innleggType(conn, innlegg)
    return jsonify(innlegg)


# ---- AVTALER ----
# Henter avtaler for bedrift med bid
@app.route("/avtaler", methods=["GET"])
def getAvtaler():
    conn = get_db()
    bid = request.args.get("bid", "")
    return jsonify(get_deals_by_bid(conn, bid))

# Henter alle avtaler og legger til en dictionary med bedriftsinfo for bid
@app.route("/alleAvtaler", methods=["GET"])
def getAllAvtaler():
    conn = get_db()
    avtaler = get_deals(conn)
    for deal in avtaler:
        deal["bid"] = get_company_by_bid(conn, deal["bid"])
    return jsonify(avtaler)


# ---- EDIT ---
# Endrer bedriftsinformasjon
@app.route("/editInfo", methods=["POST"])
def editCompInfo():
    conn = get_db()
    edit_form = request.get_json()
    # Sjekker brukerinput 
    for key in edit_form:
        text = validate_userinput(str(edit_form[key]), key)
        if text != "Ok" and text != "":
            return jsonify(text)
    edit_company_info(conn, edit_form["bid"], edit_form["Navn"], edit_form["Telefon"], edit_form["Mail"], edit_form["Adresse"])
    return jsonify("Sucess")


# ----- BILDEOPPLASTNING -----
@app.route("/uploadImg", methods=["POST"])
def upload():
    conn = get_db()
    # Get the logedin user and company for the user
    if session.get("username", None):
        username = session.get("username")
        user = get_user_by_name(get_db(),username)
    company = get_company(conn, user["userid"])
    bid = company["bid"]
    # Get the uploaded file
    file = request.files['image']
    if file.filename == "":
        return jsonify("")
    # Sjekker om det er et sikkert filnavn, og endrer det til et sikkert. Setter filnavnet med bedriftsid og sjekker om 
    # det ligger et path for bedriften i databasen.
    # Lagrer det ny bilde for bedriften og lagrer pathen i databasen.
    if file and allowed_file(file.filename):
        secured_filename = secure_filename(file.filename)
        org_name = secured_filename.split(".")
        name = org_name[0] + "_" + str(bid)
        delete_exsisting(conn, bid)
        stream = file.read()
        img = Image.open(BytesIO(stream))
        type = file.filename.split(".")
        img_path = upload_forlder + name + "." + type[-1]
        img.save(img_path)
        add_img(conn, img_path, bid)
        path = get_img_from_bid(conn, bid)
        return jsonify(path["filename"])
    return jsonify("")


@app.route("/", methods=["GET"])
def index():
    return app.send_static_file("index.html")

if __name__ == "__main__":
    app.run()
