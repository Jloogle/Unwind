import datetime
import os
import time

import httplib2
import telebot
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from pycbrf.toolbox import ExchangeRates
from sqlalchemy import select

from models import Orders, Session, create_table
from settings import ID_SHEETS, PERIOD, TELEGRAM_CHAT_ID, TELEGRAM_TOKEN


def get_service():
    """ Подключение к сервису google api """
    creeds_json = os.path.dirname(__file__) + "/creeds/creeds.json"
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creeds_service = ServiceAccountCredentials.from_json_keyfile_name(
        creeds_json, scopes
    ).authorize(httplib2.Http())
    return build('sheets', 'v4', http=creeds_service)


def get_values():
    """ Получение списка данных из google sheets таблицы"""
    service = get_service()
    sheet = service.spreadsheets()
    resp = sheet.values().batchGet(spreadsheetId=ID_SHEETS,
                                   ranges=["Лист1"]).execute()
    values = resp.get('valueRanges')[0].get('values')
    return values


if __name__ == '__main__':
    create_table()
    bot = telebot.TeleBot(TELEGRAM_TOKEN)
    with Session() as db_session:
        while True:
            try:
                values = get_values()

                # получаем курс доллара
                date_now = datetime.date.today()
                usd_rates = ExchangeRates(f'{date_now}')['USD'].value

                # получение номеров ордеров из google sheets и списка ордеров
                # для проверки, не удалили ли их из таблицы
                values_order_numbers = (
                    value[1] if len(value) < 4 else None for value in values
                )
                old_orders = db_session.execute(select(Orders)).scalars()
                for order in old_orders:
                    if order.order_number not in values_order_numbers:
                        db_session.delete(order)

                for _ in range(1, len(values)):
                    if len(values[_]) < 4:
                        # если на момент получения данных из google sheets
                        # новая запись была не полностью внесена, пропускаем её
                        continue
                    order = Orders(values[_], usd_rates)
                    query_order = select(Orders).where(
                        Orders.order_number.__eq__(order.order_number)
                    )
                    order_in_base = db_session.execute(query_order).scalar()
                    if order.delivery_date < date_now:
                        bot.send_message(
                            TELEGRAM_CHAT_ID,
                            f'У ордера с номером {order.order_number} '
                            'закончился срок поставки')
                    if not order_in_base:
                        db_session.add(order)
                    else:
                        order_in_base.price_rub = order.price_rub
                        order_in_base.price_usd = order.price_usd
                        order_in_base.delivery_date = order.delivery_date
                        db_session.add(order_in_base)
                db_session.commit()
            except Exception as e:
                db_session.rollback()
                print(e)
                break
            time.sleep(PERIOD)
