import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
from dotenv import load_dotenv
from datetime import datetime, timedelta, date
# Set the date to 5 days ago
date = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
def message(subject="Python Notification", text="", img=None, attachment=None):
    """Build the email message with optional text, images, and attachments."""
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    # Add attachments if provided
    if attachment is not None:
        if type(attachment) is not list:
            attachment = [attachment]
        for one_attachment in attachment:
            if os.path.isfile(one_attachment):  # Ensure file exists
                with open(one_attachment, 'rb') as f:
                    file = MIMEApplication(f.read(), name=os.path.basename(one_attachment))
                    file['Content-Disposition'] = f'attachment; filename="{os.path.basename(one_attachment)}"'
                    msg.attach(file)
            else:
                print(f"Attachment file not found: {one_attachment}")
                
    return msg

def main():
    """Main function to send an email with attachments."""
    # Initialize connection to the email server (Gmail)
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    load_dotenv()

    # Login with your email and password stored in environment variables
    smtp.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASS'))

    # Define the message details
    msg = message(
        subject="Good!",
        text="Hi there!",
        attachment=["/home/naveen/Projects/News_analyzer/server/assets/mean_polarity.csv",f"/home/naveen/Projects/News_analyzer/server/assets/{date}.csv"]
    )

    # List of recipients
    to = ["praveenkumar.ad21@bitsathy.ac.in"]

    # Send the email
    smtp.sendmail(from_addr="naveenbharathi.it21@bitsathy.ac.in", to_addrs=to, msg=msg.as_string())

    # Close the SMTP connection
    smtp.quit()

# Allow the script to be run standalone or imported as a module
if __name__ == "__main__":
    main()
