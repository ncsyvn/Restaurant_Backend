from flask import Blueprint, request
from webargs.flaskparser import FlaskParser
from marshmallow import fields
from src.models import Product, BillDetail, Bill
from src.utils import object_as_dict, create_fail, create_success, get_fail, get_success, \
    update_fail, update_success, delete_fail, delete_success, product_amount_sell_day
from src.extensions import db
import datetime

parser = FlaskParser()
api = Blueprint('statistic', __name__)

@api.route('/day', methods=['GET'])
def statistic_by_day():
    page_size = request.args.get('page_size', 25, type=int)
    page_number = request.args.get('page_number', 1, type=int)

    Datetime = request.args.get('Datetime')
    if Datetime is not None:
        Datetime = datetime.datetime.strptime(Datetime, '%Y-%m-%d %H:%M:%S')

    row_bill_detail = BillDetail.query.all()
    result_bill_detail = [object_as_dict(x) for x in row_bill_detail]
    row_bills = Bill.query.all()
    result_bills = [object_as_dict(x) for x in row_bills]

    buy_today = 0
    sell_today = 0
    revenue_today = 0
    buy_previous = 0
    sell_previous = 0
    revenue_previous = 0

    for x in result_bill_detail:
        for y in result_bills:
            if x["BillId"] == y['BillId'] and (y['Datetime'].date()-Datetime.date()).days == 0:
                if y["Type"] == 0:
                    buy_today += x["Amount"]
                    revenue_today -= x["Amount"] * x["Price"]
                elif y["Type"] == 1:
                    sell_today += x["Amount"]
                    revenue_today += x["Amount"] * x["Price"]
            elif x["BillId"] == y['BillId'] and (y['Datetime'].date()-Datetime.date()).days == -1:
                if y["Type"] == 0:
                    buy_previous += x["Amount"]
                    revenue_previous -= x["Amount"] * x["Price"]
                elif y["Type"] == 1:
                    sell_previous += x["Amount"]
                    revenue_previous += x["Amount"] * x["Price"]
    result = {
        "soMua": buy_today,
        "soBan": sell_today,
        "doanhThu": revenue_today,
        "soMuaTang": buy_today - buy_previous,
        "soBanTang": sell_today - sell_previous,
        "doanhThuTang": revenue_today/revenue_previous if revenue_previous!=0 else 100
    }
    return get_success(result)


    # if DatetimeStart is not None:
    #     i = 0
    #     while i < len(result):
    #         if (result[i]['Datetime'] - DatetimeStart).days < 0:
    #             result.pop(i)
    #         else:
    #             i += 1
    #
    # if DatetimeEnd is not None:
    #     i = 0
    #     while i < len(result):
    #         if (result[i]['Datetime'] - DatetimeEnd).days > 0:
    #             result.pop(i)
    #         else:
    #             i += 1
    # start_index = page_size * (page_number - 1)
    # end_index = page_size * page_number
    # if start_index >= len(result):
    #     result = []
    # elif end_index > len(result):
    #     result = result[start_index: len(result)]
    # else:
    #     result = result[start_index: end_index]
    # return get_success(result)
