from flask_sqlalchemy import SQLAlchemy
from my_app import app


db = SQLAlchemy(app)


class Currency(db.Model):
    __tablename__ = 'currency'

    id = db.Column(db.Integer, primary_key=True)
    cur_name = db.Column(db.String(80), nullable=False)
    cur_course = db.Column(db.Numeric, nullable=False)
    cur_code = db.Column(db.String(80), nullable=False)
    cur_nominal = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __str__(self):
        return self.cur_name
