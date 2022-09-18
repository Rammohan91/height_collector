from distutils.log import error
from unicodedata import category
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/height_collector'
db = SQLAlchemy(app)

class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    email_ = db.Column(db.String(120), unique=True)
    height_ = db.Column(db.Integer)

    def __init__(self, email_, height_):
        self.email_ = email_
        self.height_ = height_

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    if request.method=='POST':
        email = request.form["email_name"]
        height = request.form["height_name"]


        if db.session.query(Data).filter(Data.email_ == email).count() == 0:
            data = Data(email_=email, height_=height)
            db.session.add(data)
            db.session.commit()
            average_height = db.session.query(func.avg(Data.height_)).scalar()
            average_height = round(average_height, 1)
            send_email(email, height, average_height)
            return render_template("success.html")
    return render_template('index.html', text="Alert: Seems like we have got something already from this address.!",category='error')

if __name__ == '__main__':
    app.run(debug = True)