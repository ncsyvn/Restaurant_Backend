from flask import Blueprint, request
from webargs.flaskparser import FlaskParser
from marshmallow import fields
from src.models import Bill
from src.utils import object_as_dict, create_fail, create_success, get_fail, get_success, \
    update_fail, update_success, delete_fail, delete_success
from src.extensions import db
import datetime

parser = FlaskParser()
api = Blueprint('bills', __name__)


@api.route('', methods=['GET'])
def get_all_bill():
    page_size = request.args.get('page_size', 25, type=int)
    page_number = request.args.get('page_number', 1, type=int)

    try:
        max_length = len(Bill.query.order_by(Bill.BillId).all())
        if max_length - page_size * (page_number-1) < 1:
            result = []
        else:
            result = [object_as_dict(x) for x in Bill.query.order_by(Bill.BillId).
                paginate(page=page_number, per_page=page_size).items]
        return get_success(result)
    except:
        return get_fail()
    return get_fail()


@api.route('/<BillId>', methods=['GET'])
def get_Bill_by_id(BillId):
    try:
        row = Bill.query.get(BillId)
        result = object_as_dict(row)
        return get_success(result)
    except:
        return get_fail()
    return get_fail()


@api.route('/search', methods=['GET'])
def search():
    page_size = request.args.get('page_size', 25, type=int)
    page_number = request.args.get('page_number', 1, type=int)
    TotalMoneyStart = request.args.get('TotalMoneyStart', type=str)
    TotalMoneyEnd = request.args.get('TotalMoneyEnd', type=str)
    Type = request.args.get("Type", type=int)

    DatetimeStart = request.args.get('DatetimeStart')
    if DatetimeStart is not None and DatetimeStart != "":
        DatetimeStart = datetime.datetime.strptime(DatetimeStart, '%Y-%m-%d')

    DatetimeEnd = request.args.get('DatetimeEnd')
    if DatetimeEnd is not None and DatetimeStart != "":
        DatetimeEnd = datetime.datetime.strptime(DatetimeEnd, '%Y-%m-%d')

    row = Bill.query.filter(Bill.Type == Type)

    result = [object_as_dict(x) for x in row]

    if TotalMoneyStart is not None and TotalMoneyStart != "":
        TotalMoneyStart = float(TotalMoneyStart)
        i = 0
        while i < len(result):
            if result[i]['TotalMoney'] < TotalMoneyStart:
                result.pop(i)
            else:
                i += 1

    if TotalMoneyEnd is not None and TotalMoneyEnd != "":
        TotalMoneyEnd = float(TotalMoneyEnd)
        i = 0
        while i < len(result):
            if result[i]['TotalMoney'] > TotalMoneyEnd:
                result.pop(i)
            else:
                i += 1

    if DatetimeStart is not None and DatetimeStart != "":
        i = 0
        while i < len(result):
            if (result[i]['Datetime'] - DatetimeStart).days < -1:
                result.pop(i)
            else:
                i += 1

    if DatetimeEnd is not None and DatetimeStart != "":
        i = 0
        while i < len(result):
            if (result[i]['Datetime'] - DatetimeEnd).days > 1:
                result.pop(i)
            else:
                i += 1
    start_index = page_size * (page_number - 1)
    end_index = page_size * page_number
    if start_index >= len(result):
        result = []
    elif end_index > len(result):
        result = result[start_index: len(result)]
    else:
        result = result[start_index: end_index]
    return get_success(result)


@api.route('', methods=['POST'])
def post():
    params = {
        'Type': fields.Integer(),
        'Datetime': fields.DateTime(),
        'TotalMoney': fields.Float(),
        'Description': fields.String(),
        'Weather': fields.Integer(),
        'Temperature': fields.Integer()
    }

    json_data = parser.parse(params)
    Type = json_data.get('Type')
    Datetime = json_data.get('Datetime')
    TotalMoney = json_data.get('TotalMoney')
    Description = json_data.get('Description')
    Weather = json_data.get('Weather')
    Temperature = json_data.get('Temperature')

    print(json_data)
    new_values = Bill(Type=Type, Datetime=Datetime, TotalMoney=TotalMoney, Description=Description, Weather=Weather,
                      Temperature=Temperature)
    try:
        db.session.add(new_values)
        db.session.commit()
        all_bills = Bill.query.order_by(Bill.BillId).all()
        max = 0
        for bill in all_bills:
            if bill.BillId > max:
                max = bill.BillId
        return {
            "status": True,
            "msg": "Thêm mới thành công",
            "data": {
                "BillId": max
            }
        }
    except:
        return create_fail()
    return create_fail()


@api.route('/<BillId>', methods=['PUT'])
def put(BillId):
    try:
        row = Bill.query.get(BillId)
    except:
        return update_fail()
    json_data = request.get_json()
    Type = json_data.get('Type')
    Datetime = json_data.get('Datetime')
    TotalMoney = json_data.get('TotalMoney')
    Description = json_data.get('Description')
    Weather = json_data.get('Weather')
    Temperature = json_data.get('Temperature')

    Datetime = str(Datetime)

    if Type is not None:
        row.Type = Type
    if Datetime is not None:
        try:
            day = Datetime[:10]
            hour = Datetime[11:19]
            row.Datetime = datetime.datetime.strptime(day + ' ' + hour, '%Y-%m-%d %H:%M:%S')
        except:
            return update_fail()
    if TotalMoney is not None:
        row.TotalMoney = TotalMoney
    if Description is not None:
        row.Description = Description
    else:
        row.Description = ""
    if Weather is not None:
        row.Weather = Weather
    if Temperature is not None:
        row.Temperature = Temperature
    try:
        db.session.commit()
        return update_success()
    except:
        return update_fail()
    return update_fail()


@api.route('/<BillId>', methods=['DELETE'])
def delete(BillId):
    row = Bill.query.get(BillId)
    try:
        db.session.delete(row)
        db.session.commit()
        return delete_success()
    except:
        return delete_fail()
    return delete_fail()
