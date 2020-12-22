from src.extensions import db

class Product(db.Model):
    __tablename__ = 'product'

    ProductId = db.Column(db.Integer, primary_key=True, nullable=False)
    ProductName = db.Column(db.String(255))
    Thumbnail = db.Column(db.String(255))
    ModelID = db.Column(db.Integer)


class Bill(db.Model):
    __tablename__ = 'bill'

    BillId = db.Column(db.Integer, primary_key=True, nullable=False)
    Type = db.Column(db.Integer)
    TotalMoney = db.Column(db.Float)
    Description = db.Column(db.String(1000))
    Datetime = db.Column(db.DateTime())
    Weather = db.Column(db.Integer)
    Temperature = db.Column(db.Integer)


class BillDetail(db.Model):
    __tablename__ = 'bill_detail'

    BillDetailId = db.Column(db.Integer, primary_key=True, nullable=False)
    BillId = db.Column(db.Integer, nullable=False)
    ProductId = db.Column(db.Integer, nullable=False)
    TotalMoney = db.Column(db.Float)
    Price = db.Column(db.Float)
    Amount = db.Column(db.Integer)
