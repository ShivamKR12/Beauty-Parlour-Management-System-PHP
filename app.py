from flask import Flask, render_template, session, redirect, url_for, jsonify, request, flash
import mysql.connector
import random
from werkzeug.security import check_password_hash, generate_password_hash
import hashlib

app = Flask(__name__)
app.secret_key = "super-secret-key"

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="bpmsdb"
    )


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/api/aboutus")
def aboutus_data():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT PageTitle, PageDescription FROM tblpage WHERE PageType='aboutus'")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(rows)


@app.route("/appointment/<aptnumber>")
def appointment_detail(aptnumber):
    # Login check (PHP session replacement)
    if 'bpmsuid' not in session:
        return redirect(url_for('logout'))

    return render_template("appointment_detail.html", aptnumber=aptnumber)


@app.route("/api/appointment/<aptnumber>")
def appointment_data(aptnumber):
    if 'bpmsuid' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    query = """
    SELECT 
        tbluser.FirstName,
        tbluser.LastName,
        tbluser.Email,
        tbluser.MobileNumber,
        tblbook.AptNumber,
        tblbook.AptDate,
        tblbook.AptTime,
        tblbook.BookingDate,
        tblbook.Status
    FROM tblbook
    JOIN tbluser ON tbluser.ID = tblbook.UserID
    WHERE tblbook.AptNumber = %s
    """

    cursor.execute(query, (aptnumber,))
    row = cursor.fetchone()

    cursor.close()
    db.close()

    return jsonify(row)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- BOOK APPOINTMENT PAGE ----------------
@app.route("/book-appointment")
def book_appointment():
    if 'bpmsuid' not in session:
        return redirect(url_for('logout'))

    return render_template("book_appointment.html")


# ---------------- CONTACT INFO API ----------------
@app.route("/api/contact-info")
def contact_info():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tblpage WHERE PageType='contactus'")
    data = cursor.fetchone()

    cursor.close()
    db.close()

    return jsonify(data)


# ---------------- CREATE APPOINTMENT ----------------
@app.route("/api/book-appointment", methods=["POST"])
def create_appointment():
    if 'bpmsuid' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json

    uid = session['bpmsuid']
    adate = data['adate']
    atime = data['atime']
    message = data['message']
    aptnumber = random.randint(100000000, 999999999)

    db = get_db_connection()
    cursor = db.cursor()

    query = """
    INSERT INTO tblbook (UserID, AptNumber, AptDate, AptTime, Message)
    VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(query, (uid, aptnumber, adate, atime, message))
    db.commit()

    cursor.close()
    db.close()

    session['aptno'] = aptnumber

    return jsonify({"success": True, "aptno": aptnumber})


@app.route("/thank-you")
def thank_you():
    return render_template("thank_you.html", aptno=session.get('aptno'))


# ---------------- BOOKING HISTORY PAGE ----------------
@app.route("/booking-history")
def booking_history():
    if 'bpmsuid' not in session:
        return redirect(url_for('logout'))

    return render_template("booking_history.html")


# ---------------- BOOKING HISTORY API ----------------
@app.route("/api/booking-history")
def booking_history_api():
    if 'bpmsuid' not in session:
        return jsonify([])

    userid = session['bpmsuid']

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    query = """
    SELECT
        tblbook.AptNumber,
        tblbook.AptDate,
        tblbook.AptTime,
        tblbook.Status
    FROM tblbook
    WHERE tblbook.UserID = %s
    ORDER BY tblbook.ID DESC
    """

    cursor.execute(query, (userid,))
    rows = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(rows)


# ---------------- CHANGE PASSWORD PAGE ----------------
@app.route("/change-password")
def change_password():
    if 'bpmsuid' not in session:
        return redirect(url_for('logout'))

    return render_template("change_password.html")


# ---------------- CHANGE PASSWORD API ----------------
@app.route("/api/change-password", methods=["POST"])
def change_password_api():
    if 'bpmsuid' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    userid = session['bpmsuid']
    current_password = data['currentpassword']
    new_password = data['newpassword']

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT Password FROM tbluser WHERE ID = %s",
        (userid,)
    )
    user = cursor.fetchone()

    if not user or not check_password_hash(user['Password'], current_password):
        return jsonify({"success": False, "message": "Current password is wrong"})

    hashed_password = generate_password_hash(new_password)

    cursor.execute(
        "UPDATE tbluser SET Password = %s WHERE ID = %s",
        (hashed_password, userid)
    )
    db.commit()

    cursor.close()
    db.close()

    return jsonify({"success": True})


# ---------------- CONTACT PAGE ----------------
@app.route("/contact")
def contact():
    return render_template("contact.html")


# ---------------- CONTACT INFO API ----------------
@app.route("/api/contact-info")
def contact_info():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tblpage WHERE PageType='contactus'")
    row = cursor.fetchone()

    cursor.close()
    db.close()

    return jsonify(row)


# ---------------- CONTACT FORM SUBMIT ----------------
@app.route("/api/contact", methods=["POST"])
def submit_contact():
    data = request.json

    db = get_db_connection()
    cursor = db.cursor()

    query = """
    INSERT INTO tblcontact (FirstName, LastName, Phone, Email, Message)
    VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(query, (
        data['fname'],
        data['lname'],
        data['phone'],
        data['email'],
        data['message']
    ))

    db.commit()
    cursor.close()
    db.close()

    return jsonify({"success": True})


# ---------------- FORGOT PASSWORD PAGE ----------------
@app.route("/forgot-password")
def forgot_password():
    return render_template("forgot_password.html")


# ---------------- CONTACT INFO API ----------------
@app.route("/api/contact-info")
def contact_info():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tblpage WHERE PageType='contactus'")
    data = cursor.fetchone()

    cursor.close()
    db.close()
    return jsonify(data)


# ---------------- RESET PASSWORD API ----------------
@app.route("/api/reset-password", methods=["POST"])
def reset_password():
    data = request.json

    email = data["email"]
    contactno = data["contactno"]
    password = hashlib.md5(data["newpassword"].encode()).hexdigest()

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        "SELECT ID FROM tbluser WHERE Email=%s AND MobileNumber=%s",
        (email, contactno)
    )

    user = cursor.fetchone()

    if user:
        cursor.execute(
            "UPDATE tbluser SET Password=%s WHERE Email=%s AND MobileNumber=%s",
            (password, email, contactno)
        )
        db.commit()
        response = {"success": True}
    else:
        response = {"success": False}

    cursor.close()
    db.close()
    return jsonify(response)


@app.route("/invoice-history")
def invoice_history():
    # Check if user is logged in
    if 'bpmsuid' not in session:
        return redirect(url_for('logout'))  # create a /logout route

    user_id = session['bpmsuid']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT DISTINCT u.ID AS uid, u.FirstName, u.LastName, u.MobileNumber,
                        i.BillingId, DATE(i.PostingDate) AS PostingDate
        FROM tbluser u
        JOIN tblinvoice i ON u.ID = i.Userid
        WHERE u.ID = %s
        ORDER BY i.ID DESC
    """, (user_id,))
    invoices = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("invoice_history.html", invoices=invoices)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email_or_contact = request.form["emailcont"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT ID, Password FROM tbluser WHERE Email=%s OR MobileNumber=%s",
            (email_or_contact, email_or_contact)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user["Password"], password):
            session["bpmsuid"] = user["ID"]
            return redirect(url_for("home"))  # redirect to home page
        else:
            flash("Invalid details. Please try again.", "danger")

    # Fetch contact info (dynamic content)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tblpage WHERE PageType='contactus'")
    contact_info = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template("login.html", contact=contact_info)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


def login_required():
    if "bpmsuid" not in session:
        return False
    return True


@app.route("/profile")
def profile():
    if not login_required():
        return redirect(url_for("logout"))

    uid = session["bpmsuid"]
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tbluser WHERE ID=%s", (uid,))
    user = cursor.fetchone()

    cursor.execute("SELECT * FROM tblpage WHERE PageType='contactus'")
    contact = cursor.fetchone()

    return render_template("profile.html", user=user, contact=contact)


@app.route("/update-profile", methods=["POST"])
def update_profile():
    if not login_required():
        return jsonify({"status": "unauthorized"})

    uid = session["bpmsuid"]
    fname = request.form["firstname"]
    lname = request.form["lastname"]

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE tbluser SET FirstName=%s, LastName=%s WHERE ID=%s",
        (fname, lname, uid)
    )
    db.commit()

    return jsonify({"status": "success"})


if __name__ == "__main__":
    app.run(debug=True)
