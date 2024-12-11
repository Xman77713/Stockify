import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests

from src.models.exception import mailNotReached


def sendMail1(mailReceiver, downloadLink, apiKey, uniqueLink, expirationDate, filename):
    expirationDate = expirationDate.strftime("%d/%m/%Y à %H:%M:%S")

    separator = "-----------------------------------------------------------------"
    message = f"Hello,\nVoici un lien pour télécharger {filename} :\n{separator}\n{downloadLink}\n{separator}\n"
    if uniqueLink:
        message += "Attention ce fichier ne peut être télécharger qu'une seule fois !"
    message += f"\nExpire le {expirationDate}\n\nBon/Bonne [insérer le moment de la journée]\nLa team Stockify"

    return requests.post(
        "https://api.mailgun.net/v3/sandbox296bee9d2d684acca490f81325831fe9.mailgun.org/messages",
        auth=("api", apiKey),
        data={"from": "noreply@stockify.esiea.fr",
              "to": [mailReceiver],
              "subject": "On vous a envoyé un fichier",
              "text": message})

def sendMail(mailReceiver, downloadLink, mdpPassword, uniqueLink, expirationDate, filename):
    try:
        expirationDate = expirationDate.strftime("%d/%m/%Y à %H:%M:%S")

        separator = "-----------------------------------------------------------------"
        message = f"Hello,\nVoici un lien pour télécharger {filename} :\n{separator}\n{downloadLink}\n{separator}\n"
        if uniqueLink:
            message += "Attention ce fichier ne peut être téléchargé qu'une seule fois !"
        message += f"\nExpire le {expirationDate}\n\nBon/Bonne [insérer le moment de la journée]\nLa team Stockify"

        emailfrom = "stockifyesiea@gmail.com"
        username = emailfrom
        password = mdpPassword
        msg = MIMEMultipart()
        msg["From"] = emailfrom
        msg["To"] = mailReceiver
        msg["Subject"] = "On vous a envoyé un fichier !!"

        msg.attach(MIMEText(message))
        server = smtplib.SMTP("smtp.gmail.com:587")
        server.starttls()
        server.login(username,password)
        server.sendmail(emailfrom, mailReceiver, msg.as_string())
        server.quit()
    except Exception as e:
        raise mailNotReached