from flask import Blueprint, request
from webargs.flaskparser import FlaskParser
from marshmallow import fields
from src.models import BillDetail
from src.utils import object_as_dict, create_fail, create_success, get_fail, get_success, \
    update_fail, update_success, delete_fail, delete_success
from src.extensions import db
import random


parser = FlaskParser()
api = Blueprint('bill_detail', __name__)


@api.route('', methods=['GET'])
def get_all_bill_detail():
    page_size = request.args.get('page_size', 25, type=int)
    page_number = request.args.get('page_number', 1, type=int)

    try:
        max_length = len(BillDetail.query.order_by(BillDetail.BillDetailId).all())
        if max_length - page_size * (page_number-1) < 1:
            result = []
        else:
            result = [object_as_dict(x) for x in BillDetail.query.order_by(BillDetail.BillDetailId).
                paginate(page=page_number, per_page=page_size).items]
        return get_success(result)
    except:
        return get_fail()
    return get_fail()


@api.route('/<BillDetailId>', methods=['GET'])
def get_BillDetail_by_id(BillDetailId):
    try:
        row = BillDetail.query.get(BillDetailId)
        result = object_as_dict(row)
        return get_success(result)
    except:
        return get_fail()
    return get_fail()


@api.route('/generate_amount', methods=['GET'])
def generate_amount():
    try:
        ProductId = request.args.get('ProductId', type=int)
        Weather = request.args.get('Weather', type=int)
        Temperature = request.args.get('Temperature', type=float)
        return get_success(random.randint(60, 90))
    except:
        return get_fail()
    return get_fail()


@api.route('/search_by_bill_id/<BillId>', methods=['GET'])
def search_by_bill_id(BillId):
    try:
        row = BillDetail.query.filter(BillDetail.BillId == BillId)
        result = [object_as_dict(x) for x in row]
        return get_success(result)
    except:
        return get_fail()
    return get_fail()


@api.route('', methods=['POST'])
def post():
    params = {
        'BillId': fields.Integer(),
        'ProductId': fields.Integer(),
        'TotalMoney': fields.Float(),
        'Price': fields.Float(),
        'Amount': fields.Integer(),
    }

    json_data = parser.parse(params)
    BillId = json_data.get('BillId')
    ProductId = json_data.get('ProductId')
    TotalMoney = json_data.get('TotalMoney')
    Price = json_data.get('Price')
    Amount = json_data.get('Amount')

    new_values = BillDetail(BillId=BillId, ProductId=ProductId, TotalMoney=TotalMoney, Price=Price, Amount=Amount)
    try:
        db.session.add(new_values)
        db.session.commit()
        return create_success()
    except:
        return create_fail()
    return create_fail()



@api.route('/<BillDetailId>', methods=['PUT'])
def put(BillDetailId):
    try:
        row = BillDetail.query.get(BillDetailId)
    except:
        return update_fail()
    params = {
        'BillDetailId': fields.Integer(),
        'BillId': fields.Integer(),
        'ProductId': fields.Integer(),
        'TotalMoney': fields.Float(),
        'Price': fields.Float(),
        'Amount': fields.Integer(),
    }

    json_data = parser.parse(params)
    BillId = json_data.get('BillId')
    ProductId = json_data.get('ProductId')
    TotalMoney = json_data.get('TotalMoney')
    Price = json_data.get('Price')
    Amount = json_data.get('Amount')

    if BillId is not None:
        row.BillId = BillId
    if ProductId is not None:
        row.ProductId = ProductId
    if TotalMoney is not None:
        row.TotalMoney = TotalMoney
    if Price is not None:
        row.Price = Price
    if Amount is not None:
        row.Amount = Amount
    try:
        db.session.commit()
        return update_success()
    except:
        return update_fail()
    return update_fail()


@api.route('/<BillDetailId>', methods=['DELETE'])
def delete(BillDetailId):
    row = BillDetail.query.get(BillDetailId)
    try:
        db.session.delete(row)
        db.session.commit()
        return delete_success()
    except:
        return delete_fail()
    return delete_fail()
