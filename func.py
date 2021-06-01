from flask import g, session
from setup_db import *
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
upload_forlder = "static/img/bedrifter/"

# Get database
def get_db():
    if not hasattr(g, "_database"):
        print("create connection")
        g._database = sqlite3.connect("database.db")
    return g._database

def get_user():
    conn = get_db()
    username = session.get("username")
    return get_user_by_name(conn, username)
    
# Checks if username-password combination is valid
def valid_login(username, password):
    conn = get_db()
    hash = get_hash_for_login(conn, username)
    if hash != None:
        return check_password_hash(hash, password)
    return False

# Funskjon som sjekker brukerinput
# Alle input må ha mer enn 3 tegn, med unntak av telfon og passord som må ha 8.
def validate_userinput(userinput, key):
    # List with special characters that are not allowed in input field
    avoid = ['#', '$', '%', '=', '{', '}', '[', ']', '\\', '*', '^', '¨', '~', '§', '>', '<']
    if key == "bid":
        return ""
    if userinput == None:
        return ""
    if key == "Brukernavn":
        userinput = userinput.strip()
    for char in avoid:
        if char in userinput:
            return key + " tillatter ikke spessialtegn, prøv igjen!"
    if key == "Passord" or key == "Telefon":
        if len(userinput) < 8:
            return key + " må ha minst 8 tegn!"
    if len(userinput) < 3:
        return key + " må ha minst 3 tegn!"
    return "Ok"

# Funksjon som sjekker om det er et innlegg eller en stillingsannonse
def innleggType(conn, innlegg):
    for post in innlegg:
        if post["type"] == "innlegg":
            post["userid"] = get_mld(conn, post["userid"])
        else:
            post["userid"] = get_company(conn, post["userid"])

# Funksjon som sjekker om det opplastede bildet har et lovlig filformat
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Funskjon som sjekker om det ligger et ekisterende bilde med et annet format for bedriften - og sletter det
def delete_exsisting(conn, bid):
    company = get_company_by_bid(conn, bid)
    if company["filename"] != None:
        os.remove(company["filename"])