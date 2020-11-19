from flask import Flask, render_template, redirect, request


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://admin:admin@localhost:5432/exchange_data'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False






