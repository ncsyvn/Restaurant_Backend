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
    TotalMoneyStart = request.args.get('TotalMoneyStart', type=float)
    TotalMoneyEnd = request.args.get('TotalMoneyEnd', type=float)

    DatetimeStart = request.args.get('DatetimeStart')
    if DatetimeStart is not None:
        DatetimeStart = datetime.datetime.strptime(DatetimeStart, '%Y-%m-%d %H:%M:%S')

    DatetimeEnd = request.args.get('DatetimeEnd')
    if DatetimeEnd is not None:
        DatetimeEnd = datetime.datetime.strptime(DatetimeEnd, '%Y-%m-%d %H:%M:%S')

    row = Bill.query.order_by(Bill.BillId).all()
    result = [object_as_dict(x) for x in row]

    if TotalMoneyStart is not None:
        i = 0
        while i < len(result):
            if result[i]['TotalMoney'] < TotalMoneyStart:
                result.pop(i)
            else:
                i += 1

    if TotalMoneyEnd is not None:
        i = 0
        while i < len(result):
            if result[i]['TotalMoney'] > TotalMoneyEnd:
                result.pop(i)
            else:
                i += 1

    if DatetimeStart is not None:
        i = 0
        while i < len(result):
            if (result[i]['Datetime'] - DatetimeStart).days < 0:
                result.pop(i)
            else:
                i += 1

    if DatetimeEnd is not None:
        i = 0
        while i < len(result):
            if (result[i]['Datetime'] - DatetimeEnd).days > 0:
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
        'Description': fields.String()
    }

    json_data = parser.parse(params)
    Type = json_data.get('Type')
    Datetime = json_data.get('Datetime')
    TotalMoney = json_data.get('TotalMoney')
    Description = json_data.get('Description')

    new_values = Bill(Type=Type, Datetime=Datetime, TotalMoney=TotalMoney, Description=Description)
    try:
        db.session.add(new_values)
        db.session.commit()
        return create_success()
    except:
        return create_fail()
    return create_fail()


@api.route('/<BillId>', methods=['PUT'])
def put(BillId):
    try:
        row = Bill.query.get(BillId)
    except:
        return update_fail()
    params = {
        'Type': fields.Integer(),
        'Datetime': fields.DateTime(),
        'TotalMoney': fields.Float(),
        'Description': fields.String()
    }

    json_data = parser.parse(params)
    Type = json_data.get('Type')
    Datetime = json_data.get('Datetime')
    TotalMoney = json_data.get('TotalMoney')
    Description = json_data.get('Description')

    if Type is not None:
        row.Type = Type
    if Datetime is not None:
        row.Datetime = Datetime
    if TotalMoney is not None:
        row.TotalMoney = TotalMoney
    if Type is not None:
        row.Description = Description
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
