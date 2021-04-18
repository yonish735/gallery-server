import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_token(send_to_email, token):
    """
    Send an email with restoration code
    :param send_to_email: addressee
    :param token: restoration code
    """
    # Build message and subject
    message = 'This is your verification code: %s' % token
    subject = 'This is your verification code'

    # Build an email
    from_email = 'yonialbumshare@gmail.com'
    password = 'yonialbum'
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = send_to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Connect to SMTP server and send the email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, send_to_email, text)
    server.quit()
