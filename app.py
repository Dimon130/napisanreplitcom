import os
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "wedding_invitation_key"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL") or "sqlite:///wedding.db"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

db.init_app(app)

# Import models after db initialization
from models import RSVP

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rsvp', methods=['POST'])
def rsvp():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        guests = int(request.form.get('guests', 1))
        attending = request.form.get('attending') == 'yes'
        message = request.form.get('message', '')

        new_rsvp = RSVP(
            name=name,
            email=email,
            guests=guests,
            attending=attending,
            message=message,
            submitted_at=datetime.utcnow()
        )

        db.session.add(new_rsvp)
        db.session.commit()

        flash('Спасибо за ваш ответ!', 'success')
    except Exception as e:
        flash('Произошла ошибка. Пожалуйста, попробуйте еще раз.', 'error')
        print(f"Error: {str(e)}")

    return redirect(url_for('index'))

with app.app_context():
    db.create_all()
