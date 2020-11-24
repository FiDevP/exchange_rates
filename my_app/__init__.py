from flask import Flask


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://admin:admin@localhost:5432/exchange_data'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


import my_app.views
