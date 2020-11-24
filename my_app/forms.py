from flask_wtf import FlaskForm
from wtforms import DateField


class FilterForm(FlaskForm):
    date = DateField("Date: ", format='%Y-%m-%d')
