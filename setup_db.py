import sqlite3
from sqlite3 import Error
from flask import Flask, flash
from werkzeug.security import generate_password_hash, check_password_hash

# Styret listed in dictionary with list
STYRET = {
            "Leder": ["253467","Genette", "Vaage", "Leder"],
            "Nestleder": ["256461", "Mina", "Woeien", "Nestleder"]
        }

# sql statements for creating tables
table_users = """CREATE TABLE users(
                    userid INTEGER PRIMARY KEY,
                    username VARCHAR(20),
                    passwordhash VARCHAR(120) NOT NULL,
                    role TEXT,
                    UNIQUE(username)
                );"""

table_styret = """CREATE TABLE styret(
                    student_no INTEGER PRIMARY KEY,
                    firstname TEXT, 
                    lastname TEXT,
                    stilling TEXT,
                    userid INTEGER,
                    FOREIGN KEY (userid) REFERENCES users (userid)
                );"""

table_bedrift = """CREATE TABLE bedrift(
                    bid INTEGER PRIMARY KEY,
                    name TEXT,
                    phone_numb INTEGER,
                    mail TEXT,
                    address TEXT,
                    filename TEXT,
                    userid INTEGER,
                    FOREIGN KEY (userid) REFERENCES users (userid)
                );"""

table_deals =  """CREATE TABLE avtaler(
                    aid INTEGER PRIMARY KEY,
                    type VARCHAR(20) NOT NULL,
                    owner VARCHAR(20) NOT NULL,
                    price INTEGER,
                    start_date TEXT,
                    end_date TEXT,
                    bid INTEGER,
                    FOREIGN KEY (bid) REFERENCES bedrift (bid)
                );"""

table_post = """CREATE TABLE innlegg(
                    post_id INTEGER PRIMARY KEY,
                    text TEXT, 
                    date TEXT,
                    place TEXT,
                    type TEXT,
                    link TEXT,
                    title TEXT,
                    userid INTEGER,
                    FOREIGN KEY (userid) REFERENCES users (userid)
                );"""

# Create connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

# Create tabels
def create_table(conn, table):
    try:
        cur = conn.cursor()
        cur.execute(table)
        print("table created")
    except Error as e:
        print(e)

# Add users to database
def add_user(conn, username, hash, role="user"):
    cur = conn.cursor()
    try:
        sql = ("INSERT INTO users(username, passwordhash, role) VALUES (?,?, ?)")
        cur.execute(sql, (username, hash, role))
        conn.commit()
    except Error as err:
        print("Error: {}".format(err))
        return -1
    else:
        print("User {} created with id {}.".format(username, cur.lastrowid))
        return cur.lastrowid
    finally:
        cur.close()

# Get user by username, returns dictionary with info about user.
def get_user_by_name(conn, username):
    cur = conn.cursor()
    try:
        sql = ("SELECT userid, username, role FROM users WHERE username = ?")
        cur.execute(sql, (username,))
        for row in cur:
            (id,name,role) = row
            print(row)
            return {
                "username": name,
                "userid": id,
                "role": role
            }
        else:
            print("no user with that name")
            return {
                "username": username,
                "userid": None,
                "role": None
            }
    except Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()

# Get user details from id
def get_hash_for_login(conn, username):
    cur = conn.cursor()
    try:
        sql = ("SELECT passwordhash FROM users WHERE username=?")
        cur.execute(sql, (username,))
        for row in cur:
            (passhash,) = row
            return passhash
        else:
            return None
    except Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()

# Adds the users company to database
def add_company(conn, name, phone, address, mail, filename, id):
    cur = conn.cursor()
    try:
        sql = ("INSERT INTO bedrift (name, phone_numb, mail, address, filename, userid) VALUES (?,?,?,?,?,?)")
        cur.execute(sql, (name, phone, mail, address, filename, id))
        conn.commit()
    except Error as err:
        print("Error: {}".format(err))
        return -1
    else:
        print("Bedrift of {} created with id {}, userid {}.".format(name, cur.lastrowid, id))
        return cur.lastrowid
    finally:
        cur.close()

# Get the company from userid, returns a dict with info about the company.
# If company is not found with the given userid, it will return None in the dictionary.
def get_company(conn, userid):
    cur = conn.cursor()
    try:
        sql = ("SELECT bid, name, phone_numb, mail, address, filename, userid FROM bedrift WHERE userid=?")
        cur.execute(sql, (userid,))
        for row in cur:
            (bid, name,phone_numb,mail, address, filename, userid) = row
            return {
                "bid": bid,
                "name": name,
                "phone_numb": phone_numb,
                "mail": mail,
                "address": address,
                "filename": filename,
                "userid": userid
            }
        else:
            print("no user with that user id company")
            return {
                "bid": None,
                "name": None,
                "phone_numb": None,
                "mail": None,
                "address": None,
                "filename": None,
                "userid": userid
            }
    except Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()

def get_company_by_bid(conn, bid):
    cur = conn.cursor()
    try:
        sql = ("SELECT bid, name, phone_numb, mail, address, filename, userid FROM bedrift WHERE bid=?")
        cur.execute(sql, (bid,))
        for row in cur:
            (bid, name, phone_numb, mail, address, filename, userid) = row
            return {
                "bid": bid,
                "name": name,
                "phone_numb": phone_numb,
                "mail": mail,
                "address": address,
                "filename": filename,
                "userid": userid
            }
        else:
            print("no user with that user id company")
            return {
                "bid": bid,
                "name": None,
                "phone_numb": None,
                "mail": None,
                "address": None,
                "filename": None,
                "userid": None
            }
    except Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()


def edit_company_info(conn, bid, name, phone_numb, mail, address, filename):
    cur = conn.cursor()
    try:
        sql = ("UPDATE bedrift SET name = ?, phone_numb = ?, mail = ?, address = ?, filename = ? WHERE bid = ?")
        cur.execute(sql, (name, phone_numb, mail, address, filename, bid))
        conn.commit()
    except Error as err:
        print("Error: {}".format(err))
    else:
        print("Bedrift information updated")
    finally:
        cur.close()


# Add users as styret (admin) to the database, only done static
def add_styret(conn, student_no, firstname, lastname, stilling, userid):
    cur = conn.cursor()
    try:
        sql = ("INSERT INTO styret (student_no, firstname, lastname, stilling, userid) VALUES (?,?,?,?,?)")
        cur.execute(sql, (student_no, firstname, lastname, stilling, userid))
        conn.commit()
    except Error as err:
        print("Error: {}".format(err))
    else:
        print("{} {} added to styret as {}.".format(firstname, lastname, stilling))
    finally:
        cur.close()

# Get styremedlem from userid, returns 
def get_mld(conn, userid):
    cur = conn.cursor()
    try:
        sql = ("SELECT student_no, firstname, lastname, stilling, userid FROM styret WHERE userid=?")
        cur.execute(sql, (userid, ))
        for row in cur:
            (student_no, firstname, lastname, stilling, userid) = row
            return {
                "studentno": student_no,
                "firstname": firstname,
                "lastname": lastname,
                "stilling": stilling,
                "userid": userid
            }
        else:
            print("no user with that user id styret")
            return {
                "studentno": None,
                "firstname": None,
                "lastname": None,
                "stilling": None,
                "userid": userid
            }
    except Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()


# Insert innlegg into database, which returns the post_id
def make_post(conn, text, date, user, type="innlegg", place="", link="", title=""):
    cur = conn.cursor()
    try:
        sql = ("INSERT INTO innlegg (text, date, place, type, link, title, userid) VALUES (?,?,?,?,?,?,?)")
        cur.execute(sql, (text, date, place, type, link, title, user))
        conn.commit()
    except Error as err:
        print("Error: {}".format(err))
        return -1
    else:
        print("Post of type {} created with id {}.".format(type, cur.lastrowid))
        return cur.lastrowid
    finally:
        cur.close()

# Get posts from database and return them in a list
# ma kanskje returnere tom liste hvis error?
def get_post(conn):
    cur = conn.cursor()
    try:
        sql = ("SELECT post_id, text, date, place, type, link, title, userid FROM innlegg ORDER BY date")
        cur.execute(sql)
        posts = []
        for row in cur:
            (post_id, text, date, place, type, link, title, userid) = row
            posts.append( {
                "id": post_id,
                "text": text,
                "date": date,
                "place": place,
                "type": type,
                "link": link,
                "title": title,
                "userid": userid
            })
        if len(posts) > 1:
            posts = posts[::-1]
        return posts
    except Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()

# delete post from post_id
def delete_post(conn, post_id):
    cur = conn.cursor()
    try:
        sql = "DELETE FROM innlegg WHERE post_id=?"
        cur.execute(sql, (post_id,))
        conn.commit()
        return "Deleted"
    except Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()   

# Insert deals into database, which returns the id of the deal
def create_deals(conn, type, owner, price, start_date, end_date, bid):
    cur = conn.cursor()
    try:
        sql = ("INSERT INTO avtaler (type, owner, price, start_date, end_date, bid) VALUES (?,?,?,?,?,?)")
        cur.execute(sql, (type, owner, price, start_date, end_date, bid))
        conn.commit()
    except Error as err:
        print("Error: {}".format(err))
        return -1
    else:
        print("Deal of type {} created with id {} for company with id {}.".format(type, cur.lastrowid, bid))
        return cur.lastrowid
    finally:
        cur.close()

def get_deals(conn):
    cur = conn.cursor()
    try:
        sql = ("SELECT aid, type, owner, price, start_date, end_date, bid FROM avtaler ORDER BY type")
        cur.execute(sql)
        avtaler = []
        for row in cur:
            (aid, type, owner, price, start_date, end_date, bid) = row
            avtaler.append( {
                "aid": aid,
                "type": type,
                "owner": owner,
                "price": price,
                "start_date": start_date,
                "end_date": end_date,
                "bid": bid
            })
        return avtaler
    except Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()

# Get deal by company id, returns the deal.
def get_deals_by_bid(conn, bid):
    cur = conn.cursor()
    try:
        sql = ("SELECT aid, type, owner, price, start_date, end_date, bid FROM avtaler WHERE bid = ?")
        cur.execute(sql, (bid,))
        avtaler = []
        for row in cur:
            (aid, type, owner, price, start_date, end_date, bid) = row
            avtaler.append( {
                "aid": aid,
                "type": type,
                "owner": owner,
                "price": price,
                "start_date": start_date,
                "end_date": end_date,
                "bid": bid
            })
        return avtaler
    except Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()


def setup():
    # Create connection and create tables
    conn = create_connection("database.db")
    create_table(conn, table_users)
    create_table(conn, table_styret)
    create_table(conn, table_bedrift)
    create_table(conn, table_deals)
    create_table(conn, table_post)

    # Add styret as admin
    leder = add_user(conn, STYRET["Leder"][0], generate_password_hash("123"), "admin")
    nest = add_user(conn, STYRET["Nestleder"][0], generate_password_hash("123"), "admin")
    add_styret(conn, STYRET["Leder"][0], STYRET["Leder"][1], STYRET["Leder"][2], STYRET["Leder"][3], leder)
    add_styret(conn, STYRET["Nestleder"][0], STYRET["Nestleder"][1], STYRET["Nestleder"][2], STYRET["Nestleder"][3], nest)

    # Add static companies
    bed_user1 = add_user(conn,"sopra", generate_password_hash("123"))
    bed_user2 = add_user(conn,"kongsberg", generate_password_hash("1234"))
    bed1 = add_company(conn, "Sopra Steria", 91999801, "Address 2", "mina@mail.com", "/static/img/sopra.png", bed_user1)
    bed2 = add_company(conn, "Kongsberg Digital", 91999801, "Address 54", "mina@mail.com", "/static/img/kongsberg.jpg", bed_user2)

    # Add static posts
    # Stillingsannonser
    make_post(conn, "Vi i Sopra Steria soker nye fulltidsansatte. Mer informasjon paa linken!", "12.april 2021", bed_user1, "Heltid", "Asker")
    make_post(conn, "Perfekt jobb for deg som liker aa programmere!", "23.juni 2021", bed_user2, "Deltid", "Stavanger")
    
    # Innlegg
    make_post(conn, "Hei, alle Data og elektro studenter! Har DU lyst å være med på Wings for Life World Run og få en goodiebag?️ Søndag 9. mai kl 13:00 går startskuddet for Wings for Life World Run 2021. Wings for Life World Run er verdens eneste globale veldedighetsløp der startskuddet går likt over hele kloden. 100% av deltakeravgiften går direkte til organisasjonen Wings for Life som jobber med å gjøre ryggmargskader kurerbare. Meld deg på her:", "2021/05/04", leder, "innlegg", "", "https://www.wingsforlifeworldrun.com/en/locations/app", "Wings For Life")
    make_post(conn, "Bli med og få en skikkelig kino goodiebag!! Filmen er Hangover, og vil bli vist torsdag 13.mai klokken 20:00.", "2021/05/09", nest, "innlegg", "", "https://forms.gle/XiBvDKsN8atw92hr6", "NETFLIX PARTY!")

    #Add static deals
    create_deals(conn, "Samarbeidsavtale", "LED & ISI", "70 000", "30.02.2021", "30.02.2022", bed2)
    create_deals(conn, "Bedriftspresentasjon", "LED", "15 000", "22.03.2021", "22.06.2022", bed2)
    create_deals(conn, "Samarbeidsavtale", "LED", "40 000", "02.04.2021", "02.04.2022", bed1)

    print(get_deals_by_bid(conn, bed2))

    #edit_company_info(conn, 2, "Mina", 91999801, "Address 54", "mina@mail.com", "/static/img/kongsberg.jpg")
 
    # print(get_post(conn))
    # print(delete_post(conn, 1))
    # print(get_post(conn))

if __name__ == "__main__":
    setup()