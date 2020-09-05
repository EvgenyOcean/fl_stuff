import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_USE_TLS = True
    MAIL_PORT = 587
    MAIL_PASSWORD = os.environ.get('MAIL_PASS')
    MAIL_USERNAME = os.environ.get('MAIL_USER')