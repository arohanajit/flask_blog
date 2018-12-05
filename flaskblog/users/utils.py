import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail


def save_pic(form_pic):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pic.filename)
    pic_fn = random_hex + f_ext
    pic_path = os.path.join(current_app.root_path,
                            'static/profile_pics', pic_fn)
    output_size = (125, 125)
    i = Image.open(form_pic)
    i.thumbnail(output_size)
    i.save(pic_path)
    return pic_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreplydaemon@flask.com', recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link: {url_for('users.reset_token', token=token, _external=True)}
    If you did not make this request, Ignore this mail.
    '''
    mail.send(msg)
