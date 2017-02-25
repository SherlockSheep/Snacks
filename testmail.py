from flask import Flask
from flask.ext.mail import Mail, Message
from flask import current_app, render_template
import os

app = Flask(__name__)
app.config.update(
    DEBUG = True,
    MAIL_SERVER='smtp.qq.com',
    MAIL_PROT=25,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = '598769281@qq.com',
    MAIL_PASSWORD = 'ypxlguyxarmzbdag',
    MAIL_DEBUG = True
)

mail = Mail(app)

@app.route('/')
def index():

    msg = Message("Hi!This is a test ",sender='598769281@qq.com', recipients=['kazula@sina.cn'])
    msg.body = "This is a first email"
    with app.app_context():
        mail.send(msg)
    print "Mail sent"
    return "Sent"

if __name__ == "__main__":
    app.run()