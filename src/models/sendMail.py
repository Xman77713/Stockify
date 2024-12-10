import os
import ssl

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def sendMail(mailReceiver, downloadLink, apiKey):
    ssl._create_default_https_context = ssl._create_unverified_context

    sg = SendGridAPIClient(apiKey)
    email = Mail(
        from_email=str(os.getenv('mailSender')),
        to_emails=mailReceiver,
        subject="subject",
        plain_text_content=str(downloadLink)
    )
    response = sg.send(email)
