import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mysql.connector  # Ensure you're importing the correct MySQL connector


# from my_schedular import fetch_email
# from my_schedular import send_email


# Set up the email server

def send_email(email, Task_id, Title,due_date):

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    sender_email = 'laxmiyadav03032002pooja@gmail.com'
    sender_password = 'znuo lwzo lxgs bnpd'  # Store this in a secure manner

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = f'Pending Task: {Task_id}'

    # Email body
    body = f"Hello, here are the details for Task {Task_id}:\n\nTitle: {Title}:\n\n date:{due_date}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Start the server and login
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Upgrade the connection to secure
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, email, msg.as_string())
        print("Email sent successfully!")
        return True

    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# Usage Example
# You would call send_email with a valid email, task ID, and database connection
# conn = mysql.connector.connect(user='user', password='password', host='localhost', database='your_db')
# send_email('recipient@example.com', 123, conn)
