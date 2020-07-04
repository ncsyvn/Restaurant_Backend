from flask import Blueprint, request
from webargs.flaskparser import FlaskParser
from marshmallow import fields
from src.models import Product, BillDetail, Bill
from src.utils import object_as_dict, create_fail, create_success, get_fail, get_success, \
    update_fail, update_success, delete_fail, delete_success, product_amount_sell_day
from src.extensions import db
import datetime

parser = FlaskParser()
api = Blueprint('products', __name__)

@api.route('', methods=['GET'])
def get_all_product():
    page_size = request.args.get('page_size', 25, type=int)
    page_number = request.args.get('page_number', 1, type=int)

    """ This api gets all users.
        Returns:
        Examples::

            curl --location --request GET 'http://<sv_address>:5000/api/v1/users'
    """
    # try:
    max_length = len(Product.query.order_by(Product.ProductId).all())
    if max_length - page_size * (page_number-1) < 1:
        result = []
    else:
        result = [object_as_dict(x) for x in Product.query.order_by(Product.ProductId).
            paginate(page=page_number, per_page=page_size).items]
        for item in result:
            statistic = product_amount_sell_day(item)
            item['AmountBuyDay'] = statistic['amount_buy_day']
            item['AmountSellDay'] = statistic['amount_sell_day']
            item['AmountBuyWeek'] = statistic['amount_buy_week']
            item['AmountSellWeek'] = statistic['amount_sell_week']
            item['ProductInfor'] = [
                {
                    "a": "a"
                }
            ]
        return get_success(result)
    # except:
    #     return get_fail()
    return get_fail()


@api.route('/<ProductId>', methods=['GET'])
def get_product_by_id(ProductId):
    try:
        row = Product.query.get(ProductId)
        result = object_as_dict(row)
        return get_success(result)
    except:
        return get_fail()
    return get_fail()


@api.route('/search', methods=['GET'])
def search_by_name():
    try:
        page_size = request.args.get('page_size', 25, type=int)
        page_number = request.args.get('page_number', 1, type=int)
        ProductName = request.args.get('ProductName', type=str)
        row = Product.query.filter(Product.ProductName.contains(ProductName.strip())).\
            paginate(page=page_number, per_page=page_size).items
        result = [object_as_dict(x) for x in row]
        return get_success(result)
    except:
        return get_fail()
    return get_fail()


@api.route('', methods=['POST'])
def post():

    params = {
        'ProductName': fields.String(),
    }
    json_data = parser.parse(params)
    ProductName = json_data.get('ProductName', None).strip()
    new_values = Product(ProductName=ProductName)
    try:
        db.session.add(new_values)
        db.session.commit()
        return create_success()
    except:
        return create_fail()
    return create_fail()


@api.route('/<ProductId>', methods=['PUT'])
def put(ProductId):
    try:
        row = Product.query.get(ProductId)
    except:
        return update_fail()
    params = {
        'ProductName': fields.String(),
    }
    json_data = parser.parse(params)
    ProductName = json_data.get('ProductName', None).strip()
    if ProductName is not None:
        row.ProductName = ProductName
    try:
        db.session.commit()
        return update_success()
    except:
        return update_fail()
    return update_fail()


@api.route('/<ProductId>', methods=['DELETE'])
def delete(ProductId):
    row = Product.query.get(ProductId)
    try:
        db.session.delete(row)
        db.session.commit()
        return delete_success()
    except:
        return delete_fail()
    return delete_fail()
