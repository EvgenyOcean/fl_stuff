import os, secrets
from PIL import Image
from flask_mail import Message
from fl_todo import mail
from flask import url_for, current_app

def edit_avatar(avatar):
    new_name = secrets.token_hex(8)
    _, ext = os.path.splitext(avatar.filename)
    new_name += ext 
    im = Image.open(avatar)
    im.thumbnail((128,128))
    im.save(os.path.join(current_app.root_path, 'static/avatars', new_name))
    return new_name

def send_message(user):
    token = user.request_token()
    msg = Message('Reset Password Request', 
                  sender="noreply@demo.com",
                  recipients=[user.email])
    msg.body = f'''Please follow the link to reset your password: 
    {url_for('users.new_password', token=token, _external=True)} 
    If you have no idea whats going on, then just ignore the message. Have a good day :) 
    '''

    mail.send(msg)