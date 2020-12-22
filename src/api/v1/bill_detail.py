from flask import Blueprint, request
from webargs.flaskparser import FlaskParser
from marshmallow import fields
from src.models import BillDetail, Product
from src.utils import object_as_dict, create_fail, create_success, get_fail, get_success, \
    update_fail, update_success, delete_fail, delete_success
from src.extensions import db
import pandas as pd
import tensorflow as tf
import numpy as np
from tensorflow import keras
import datetime

parser = FlaskParser()
api = Blueprint('bill_detail', __name__)
# MODEL = joblib.load('models/linear_regression.sav')
MODEL = tf.keras.models.load_model('models/model_8_layer')

# train_stats_data = {
#             'count': [56.0, 56.0, 56.0, 56.0],
#             'mean': [5.589286, 1.785714, 27.946429, 0.410714],
#             'std': [2.877984, 0.706188, 1.444987, 0.757431],
#             'min': [1.0, 1.0, 25.0, 0.0],
#             '25%': [3.0, 1.0, 27.0, 0.0],
#             '50%': [5.5, 2.0, 28.0, 0.0],
#             '75%': [8.0, 2.0, 29.0, 1.0],
#             'max': [10.0, 3.0, 30.0, 3.0],
#             }
# train_stats = pd.DataFrame(train_stats_data,
#                   index=pd.Index(['ModelId', 'Weather', 'Temperature', 'Inventory']),
#                   columns=pd.Index(['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']))
# def norm(x):
#     return (x - train_stats['mean']) / train_stats['std']

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
            list_products = [object_as_dict(x) for x in Product.query.order_by(Product.ProductId).all()]
            for x in result:
                for y in list_products:
                    if x["ProductId"] == y["ProductId"]:
                        x["ProductName"] = y["ProductName"]
                        break
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
        ModelId = request.args.get('ProductId', type=int)
        Weather = request.args.get('Weather', type=int)
        Temperature = request.args.get('Temperature', type=int)
        Datetime = request.args.get('Datetime')
        day = Datetime[1:11]
        hour = Datetime[12:20]
        Datetime = datetime.datetime.strptime(day + ' ' + hour, '%Y-%m-%d %H:%M:%S')
        week_day = Datetime.weekday() + 2
        d = day[8:]
        m = day[5:7]
        y = day[:4]

        predict_data = pd.DataFrame([[float(d), float(m), float(y), float(week_day), float(ModelId),
                                      float(Weather), float(Temperature)]],
                                    columns=['Day', 'Month', 'Year', 'DayOfWeek', 'ModelId', 'Weather', 'Temperature'])
        print(predict_data)
        print(type(predict_data))
        result = int(MODEL.predict(predict_data)[0][0])
        print(result)
        return get_success(result)
        print(int(result))
    except:
        return get_fail()
    return get_fail()


@api.route('/search_by_bill_id/<BillId>', methods=['GET'])
def search_by_bill_id(BillId):
    try:
        row = BillDetail.query.filter(BillDetail.BillId == BillId)
        result = [object_as_dict(x) for x in row]
        list_products = [object_as_dict(x) for x in Product.query.order_by(Product.ProductId).all()]
        for x in result:
            for y in list_products:
                if x["ProductId"] == y["ProductId"]:
                    x["ProductName"] = y["ProductName"]
                    break
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
        'ProductName': fields.String()
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
