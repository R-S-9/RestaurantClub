import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .config import from_email, password

msg = MIMEMultipart()

to_email = 'rafik.saakyan.1989@mail.ru'  # Должны получать от пользователя
message = 'Сообщение сделано при помощи python'  # Сообщение которое передастся

msg.attach(MIMEText(message, 'plain'))

server = smtplib.SMTP('smtp.mail.ru: 25')
server.starttls()
server.login(from_email, password)
server.sendmail(from_email, to_email, msg.as_string())
server.quit()
