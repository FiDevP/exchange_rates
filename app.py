from flask import Flask, render_template, redirect, request

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import DBAPIError

from func_date import time_interval

from datetime import date

from zeep import Client

from lxml import etree as et


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://admin:admin@localhost:5432/exchange_data'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Currency(db.Model):
    __tablename__ = 'currency'

    id = db.Column(db.Integer, primary_key=True)
    cur_name = db.Column(db.String(80), nullable=False)
    cur_course = db.Column(db.Numeric, nullable=False)
    cur_code = db.Column(db.String(80), nullable=False)
    cur_nominal = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, default=date.today)

    def __str__(self):
        return self.cur_name


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # отлавливаем даты
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        # вызываем функцию для создания списка дат
        list_interval = time_interval(start_date, end_date)
        # создаем таблицу
        db.create_all()


        wsdl = 'http://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL'
        client = Client(wsdl=wsdl)  # Инициализируем объект подключения
        for day in list_interval:
            # отправляем запрос на веб-сервер ЦБ и ловим респонс
            with client.settings(raw_response=True):
                response_xml = str(client.service.GetCursOnDate(f'{day}').text).encode()

                root = et.fromstring(response_xml)
                # посчитаем количество элементов для итерации
                vname_list = root.xpath('//Vname/text()')

                for i in range(len(vname_list)):
                    i += 1
                    # присваиваем переменным значения элементов каждого ValuteCursOnDate
                    currency_list = root.xpath(f'//ValuteCursOnDate[{i}]/*/text()')
                    currency_name = currency_list[0].strip()
                    currency_nominal = int(currency_list[1])
                    currency_course = float(currency_list[2])
                    currency_code = currency_list[4]

                    currency = Currency(
                        cur_name=currency_name,
                        cur_code=currency_code,
                        cur_course=currency_course,
                        cur_nominal=currency_nominal,
                        date=day
                    )
                    try:
                        # Записываем значения в бд
                        db.session.add(currency)
                        db.session.commit()

                    except DBAPIError as er:
                        return "При добавлении произошла ошибка" + er.code
        return redirect('result')
    else:
        db.drop_all()
        return render_template('index.html')


@app.route('/result', methods=['GET'])
def result():
    # все значения из таблицы
    currencies = Currency.query.all()
    return render_template('result.html', currencies=currencies)


if __name__ == '__main__':
    app.run(debug=True)
