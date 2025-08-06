from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from datetime import datetime  # ✅ për datën aktuale

# Ngarko .env
load_dotenv()

app = Flask(__name__)
app.secret_key = "sekreti_yt_per_flash"

# Email settings
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")


def send_email(subject, body, to_email, html=False):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject
    msg["Reply-To"] = EMAIL_ADDRESS

    if html:
        msg.attach(MIMEText(body, "html"))
    else:
        msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/booking')
def booking():
    current_date = datetime.now().strftime('%Y-%m-%d')  # ✅ data e sotme në formatin e input
    return render_template('booking.html', current_date=current_date)


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/submit_booking', methods=['POST'])
def submit_booking():
    full_name = request.form.get('full_name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    country = request.form.get('country', '').strip()
    date = request.form.get('date', '').strip()
    adults = request.form.get('adults', '').strip()
    children = request.form.get('children', '').strip()
    tour = request.form.get('tour', '').strip()

    # Validime
    if not all([full_name, email, phone, country, date, adults, tour]):
        flash("Please fill in all required fields.", "error")
        return redirect(url_for('booking'))

    if '@' not in email:
        flash("Please enter a valid email address.", "error")
        return redirect(url_for('booking'))

    # Email për ADMIN — HTML template
    admin_body = render_template("admin_email.html",
                                 full_name=full_name,
                                 email=email,
                                 phone=phone,
                                 country=country,
                                 date=date,
                                 adults=adults,
                                 children=children,
                                 tour=tour)

    # Email për KLIENTIN — HTML template
    client_body = render_template("client_email.html",
                                  full_name=full_name,
                                  email=email,
                                  phone=phone,
                                  country=country,
                                  date=date,
                                  adults=adults,
                                  children=children,
                                  tour=tour)

    admin_sent = send_email("🧾 New Booking Received", admin_body, EMAIL_ADDRESS, html=True)
    client_sent = send_email("✅ Booking Confirmation - Hotel Kanione", client_body, email, html=True)

    if admin_sent and client_sent:
        flash("Booking was successful! A confirmation email has been sent to your address.", "success")
    elif admin_sent and not client_sent:
        flash("Booking saved, but we couldn't send the confirmation email to your address.", "error")
    else:
        flash("There was a problem saving your booking. Please try again or contact us.", "error")

    return redirect(url_for('booking'))


if __name__ == '__main__':
    app.run(debug=True)
