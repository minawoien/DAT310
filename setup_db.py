import sqlite3, os
from sqlite3 import Error
from flask import Flask, flash
from werkzeug.security import generate_password_hash, check_password_hash

# Styremedlemer i en dictionary for å enkelt kunne legge til eller endre medlemer
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

# Error meldinger og oppdateringer fra databasen blir lagt til i filen log.txt
def log_file(text):
    with open("log.txt", "a") as myfile:
        myfile.write(text)
        myfile.write("\n")

# Create connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        log_file(str(e))
    return conn

# Create tabels
def create_table(conn, table):
    try:
        cur = conn.cursor()
        cur.execute(table)
        log_file("table created")
    except Error as e:
        log_file(str(e))


# ---- USERS ----
# Legger til brukere i databasen, rolle er satt default til "user", returnerer userid
def add_user(conn, username, hash, role="user"):
    cur = conn.cursor()
    try:
        sql = ("INSERT INTO users(username, passwordhash, role) VALUES (?,?, ?)")
        cur.execute(sql, (username, hash, role))
        conn.commit()
    except Error as err:
        log_file("Error: {}".format(err))
        return -1
    else:
        log_file("User {} created with id {}.".format(username, cur.lastrowid))
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
            return {
                "username": name,
                "userid": id,
                "role": role
            }
        else:
            log_file("no user with that name")
            return {
                "username": username,
                "userid": None,
                "role": None
            }
    except Error as err:
        log_file("Error: {}".format(err))
    finally:
        cur.close()

# Get user details from username
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
        log_file("Error: {}".format(err))
    finally:
        cur.close()


# ---- COMPANY ----
# Adds the users company to database, returns companyid
def add_company(conn, name, phone, address, mail, id):
    cur = conn.cursor()
    try:
        sql = ("INSERT INTO bedrift (name, phone_numb, mail, address, userid) VALUES (?,?,?,?,?)")
        cur.execute(sql, (name, phone, mail, address, id))
        conn.commit()
    except Error as err:
        log_file("Error: {}".format(err))
        return -1
    else:
        log_file("Bedrift of {} created with id {}, userid {}.".format(name, cur.lastrowid, id))
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
            log_file("no user with that user id company")
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
        log_file("Error: {}".format(err))
    finally:
        cur.close()

# Get company information from companyid
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
            log_file("no user with that user id company")
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
        log_file("Error: {}".format(err))
    finally:
        cur.close()

# Change the company information
def edit_company_info(conn, bid, name, phone_numb, mail, address):
    cur = conn.cursor()
    try:
        sql = ("UPDATE bedrift SET name = ?, phone_numb = ?, mail = ?, address = ? WHERE bid = ?")
        cur.execute(sql, (name, phone_numb, mail, address, bid))
        conn.commit()
    except Error as err:
        log_file("Error: {}".format(err))
    else:
        log_file("Bedrift information updated")
    finally:
        cur.close()

# Add image-path to the company table from the company id
def add_img(conn, filename, bid):
    cur = conn.cursor()
    try:
        sql = ("UPDATE bedrift SET filename = ? WHERE bid = ?")
        cur.execute(sql, (filename, bid))
        conn.commit()
    except Error as err:
        log_file("Error: {}".format(err))
    else:
        log_file("Img with filename {} added to company {}.".format(filename, bid))
    finally:
        cur.close()

# Get the image-path from company id
def get_img_from_bid(conn, bid):
        cur = conn.cursor()
        try:
            sql = ("SELECT filename, bid FROM bedrift WHERE bid = ?")
            cur.execute(sql, (bid,))
            for row in cur:
                (filename, bid) = row
                return {
                    "bid": bid,
                    "filename": filename
                }
            else:
                log_file("no image with that company")
                return {
                    "bid": bid,
                    "filename": None
                }
        except Error as err:
            log_file("Error: {}".format(err))
        finally:
            cur.close()


# ---- STYRET ----
# Add users as styret (admin) to the database, only done static by running this file
def add_styret(conn, student_no, firstname, lastname, stilling, userid): 
    cur = conn.cursor()
    try:
        sql = ("INSERT INTO styret (student_no, firstname, lastname, stilling, userid) VALUES (?,?,?,?,?)")
        cur.execute(sql, (student_no, firstname, lastname, stilling, userid))
        conn.commit()
    except Error as err:
        log_file("Error: {}".format(err))
    else:
        log_file("{} {} added to styret as {}.".format(firstname, lastname, stilling))
    finally:
        cur.close()

# Get styremedlem from userid, returns information about styret
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
            log_file("no user with that user id styret")
            return {
                "studentno": None,
                "firstname": None,
                "lastname": None,
                "stilling": None,
                "userid": userid
            }
    except Error as err:
        log_file("Error: {}".format(err))
    finally:
        cur.close()

# ---- INNLEGG ----
# Insert innlegg into database, which returns the post_id
# The place, link and title is default set to an empty string
# Place is only inserted for companys, title is only for admin, and links are optional for both company and admin.
# Type is set to "innlegg" as a default value as the companys choose between differet types with select
def make_post(conn, text, date, user, type="innlegg", place="", link="", title=""):
    cur = conn.cursor()
    try:
        sql = ("INSERT INTO innlegg (text, date, place, type, link, title, userid) VALUES (?,?,?,?,?,?,?)")
        cur.execute(sql, (text, date, place, type, link, title, user))
        conn.commit()
    except Error as err:
        log_file("Error: {}".format(err))
    else:
        log_file("Post of type {} created with id {}.".format(type, cur.lastrowid))
    finally:
        cur.close()

# Get posts from database and return them in a list
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
        # Snur om rekkefølgen på postene for at de nyeste datoene kommer først
        if len(posts) > 1:
            posts = posts[::-1]
        return posts
    except Error as err:
        log_file("Error: {}".format(err))
    finally:
        cur.close()

# delete post from post_id
def delete_post(conn, post_id):
    cur = conn.cursor()
    try:
        sql = "DELETE FROM innlegg WHERE post_id=?"
        cur.execute(sql, (post_id,))
        conn.commit()
    except Error as err:
        log_file("Error: {}".format(err))
    finally:
        cur.close()   


# ---- AVTALER ----
# Insert deals into database, which returns the id of the deal
def create_deals(conn, type, owner, price, start_date, end_date, bid):
    cur = conn.cursor()
    try:
        sql = ("INSERT INTO avtaler (type, owner, price, start_date, end_date, bid) VALUES (?,?,?,?,?,?)")
        cur.execute(sql, (type, owner, price, start_date, end_date, bid))
        conn.commit()
    except Error as err:
        log_file("Error: {}".format(err))
        return -1
    else:
        log_file("Deal of type {} created with id {} for company with id {}.".format(type, cur.lastrowid, bid))
        return cur.lastrowid
    finally:
        cur.close()

# Get all deals and order them by type
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
        log_file("Error: {}".format(err))
    finally:
        cur.close()

# Get deals by company id, returns the deals.
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
        log_file("Error: {}".format(err))
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

    # Add companies
    bed_user1 = add_user(conn,"sopra", generate_password_hash("123"))
    bed_user2 = add_user(conn,"kongsberg", generate_password_hash("1234"))
    bed1 = add_company(conn, "Sopra Steria", 91999801, "Address 2", "mina@mail.com", bed_user1)
    bed2 = add_company(conn, "Kongsberg Digital", 91999801, "Address 54", "mina@mail.com", bed_user2)

    # Add img to company
    add_img(conn, "static/img/bedrifter/img_1.jpeg", bed1)

    # Add posts
    # Stillingsannonser
    make_post(conn, "Vi i Sopra Steria soker nye fulltidsansatte. Mer informasjon paa linken!", "2021-04-12", bed_user1, "Heltid", "Asker")
    make_post(conn, "Perfekt jobb for deg som liker aa programmere!", "2021-06-23", bed_user2, "Deltid", "Stavanger")
    
    # Innlegg
    make_post(conn, "Hei, alle Data og elektro studenter! Har DU lyst å være med på Wings for Life World Run og få en goodiebag?️ Søndag 9. mai kl 13:00 går startskuddet for Wings for Life World Run 2021. Wings for Life World Run er verdens eneste globale veldedighetsløp der startskuddet går likt over hele kloden. 100% av deltakeravgiften går direkte til organisasjonen Wings for Life som jobber med å gjøre ryggmargskader kurerbare. Meld deg på her:", "2021/05/04", leder, "innlegg", "", "https://www.wingsforlifeworldrun.com/en/locations/app", "Wings For Life")
    make_post(conn, "Bli med og få en skikkelig kino goodiebag!! Filmen er Hangover, og vil bli vist torsdag 13.mai klokken 20:00.", "2021/05/09", nest, "innlegg", "", "https://forms.gle/XiBvDKsN8atw92hr6", "NETFLIX PARTY!")

    #Add deals
    create_deals(conn, "Samarbeidsavtale", "LED & ISI", "70 000", "30.02.2021", "30.02.2022", bed2)
    create_deals(conn, "Bedriftspresentasjon", "LED", "15 000", "22.03.2021", "22.06.2022", bed2)
    create_deals(conn, "Samarbeidsavtale", "LED", "40 000", "02.04.2021", "02.04.2022", bed1)

if __name__ == "__main__":
    setup()