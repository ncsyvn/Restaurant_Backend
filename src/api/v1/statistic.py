from flask import Blueprint, request
from webargs.flaskparser import FlaskParser
from marshmallow import fields
from src.models import Product, BillDetail, Bill
from src.utils import object_as_dict, create_fail, create_success, get_fail, get_success, \
    update_fail, update_success, delete_fail, delete_success, product_amount_sell_day
from src.extensions import db
import datetime
from calendar import monthrange


parser = FlaskParser()
api = Blueprint('statistic', __name__)

@api.route('/day', methods=['GET'])
def statistic_by_day():
    page_size = request.args.get('page_size', 25, type=int)
    page_number = request.args.get('page_number', 1, type=int)

    Datetime = request.args.get('Datetime')
    if Datetime is not None:
        Datetime = datetime.datetime.strptime(Datetime, '%Y-%m-%d')

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
        "doanhThuTang": str(revenue_today/revenue_previous*100)[0:6] if revenue_previous != 0 else 100
    }
    return get_success(result)

@api.route('/month', methods=['GET'])
def statistic_by_month():
    try:
        page_size = request.args.get('page_size', 25, type=int)
        page_number = request.args.get('page_number', 1, type=int)

        month = int(request.args.get('month'))
        year = int(request.args.get("year"))
        amount_day_of_month = monthrange(year, month)[1]
        start_day = datetime.datetime.strptime(str(year) + "-" + str(month) + "-" + "1 " + "00:00:01", '%Y-%m-%d %H:%M:%S')

        revenues = []
        for i in range(amount_day_of_month):
            revenues.append(0)

        row_bill_detail = BillDetail.query.all()
        result_bill_detail = [object_as_dict(x) for x in row_bill_detail]
        row_bills = Bill.query.all()
        result_bills = [object_as_dict(x) for x in row_bills]
        for x in result_bill_detail:
            for y in result_bills:
                if x["BillId"] == y['BillId'] and 0 <= (y['Datetime'].date() - start_day.date()).days < amount_day_of_month:
                    if y["Type"] == 0:
                        revenues[y['Datetime'].day-1] -= x["Amount"] * x["Price"]
                    elif y["Type"] == 1:
                        revenues[y['Datetime'].day-1] += x["Amount"] * x["Price"]
        result = []
        for i in range(amount_day_of_month):
            result.append([str(i+1), revenues[i]])
        return get_success(result)
    except:
        return get_fail()
    return get_fail()

