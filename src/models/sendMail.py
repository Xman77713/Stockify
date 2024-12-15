import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.models.exception import mailNotReached

def sendMail(mailReceiver, downloadLink, mdpPassword, uniqueLink, expirationDate):
    try:
        expirationDate = expirationDate.strftime("%d/%m/%Y à %H:%M:%S")

        separator = "-----------------------------------------------------------------"
        message = f"Hello,\nVoici un lien pour télécharger votre fichier :\n{separator}\n{downloadLink}\n{separator}\n"
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