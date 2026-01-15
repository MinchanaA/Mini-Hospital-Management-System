import json
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(event, context):
    try:
        if isinstance(event.get('body'), str):
            body = json.loads(event.get('body', '{}'))
        else:
            body = event.get('body', {})
            
        recipient = body.get('recipient')
        email_type = body.get('type')
        data = body.get('data', {})

        subject = f"HMS Notification: {email_type}"
        message_body = f"Hello,\n\nThis is a notification from your Hospital Management System.\n\nType: {email_type}\nData: {data}\n\nRegards,\nHMS Team"

        # Check for credentials
        gmail_user = os.environ.get('GMAIL_USER')
        gmail_password = os.environ.get('GMAIL_APP_PASSWORD')

        if gmail_user and gmail_password:
            msg = MIMEMultipart()
            msg['From'] = gmail_user
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(message_body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(gmail_user, gmail_password)
            text = msg.as_string()
            server.sendmail(gmail_user, recipient, text)
            server.quit()
            print(f"[Real Email] Sent to {recipient}")
        else:
            print(f"[Simulated Email] Sending to {recipient} (No credentials found)")
            print(f"Subject: {subject}")
            print(f"Body: {message_body}")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Email sent successfully",
                "recipient": recipient
            })
        }
    except Exception as e:
        print(f"Error sending email: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
