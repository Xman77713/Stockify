import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def sendMail(mailReceiver, downloadLink, apiKey):

    sg = SendGridAPIClient(apiKey)
    email = Mail(
        from_email=str(os.getenv('mailSender')),
        to_emails=mailReceiver,
        subject="subject",
        plain_text_content=str(downloadLink)
    )
    response = sg.send(email)
