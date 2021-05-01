import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

from . import models


def send_token(send_to_email: str, token: str):
    """
    Send an email with restoration code
    :param send_to_email: addressee
    :param token: restoration code
    """
    # Build message and subject
    subject = 'This is your verification code'
    message = 'This is your verification code: %s' % token

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


def send_picture(request: models.Download, user: models.User):
    """
    Send an email with picture
    :param request: request with data to send email with
    :param user: user to send an email to
    """
    # Build message and subject
    subject = 'This is the picture you\'ve requested'
    picture: models.Picture = request.picture
    gallery: models.Gallery = request.gallery
    message = f"""
You've requested a picture from gallery "{gallery.title}" of \
{user.first_name} {user.last_name}\n
Title: {picture.title}\n
Description: {picture.description}\n
\n
To download the picture please see attachment
"""
    # image has format of data:image/png;base64,aVRBOw0AKg1mL9...
    # Parse it to get mimetype and base64-encoded data
    (data, image) = picture.image.split(';base64,')
    ext = data.split('/')[1]  # data:image/png
    image = base64.b64decode(image)

    # Create attachment
    img_attachment = MIMEImage(image, ext)
    img_attachment.add_header('Content-Disposition', 'attachment',
                              filename=picture.filename)

    # Build an email
    from_email = 'yonialbumshare@gmail.com'
    password = 'yonialbum'
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = request.requestor.email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    msg.attach(img_attachment)

    # Connect to SMTP server and send the email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, request.requestor.email, text)
    server.quit()
