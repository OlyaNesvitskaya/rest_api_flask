from app import db, Base, relationship, backref
from flask_jwt_extended import create_access_token
from datetime import timedelta
from passlib.hash import bcrypt
from datetime import date, datetime


class Driver(Base):
    __tablename__ = "drivers"
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.Text, default=date.today().strftime("%Y-%m-%d"))
    updated_at = db.Column(db.Text, nullable=True)


class Vehicle(Base):
    __tablename__ = "vehicles"
    id = db.Column(db.Integer(), primary_key=True)
    driver_id = db.Column(db.String, db.ForeignKey('drivers.id'))
    driver = relationship("Driver", backref=backref('vehicle'), uselist=False)
    make = db.Column(db.String(50), nullable=False, unique=True)
    model = db.Column(db.String(50), nullable=False)
    plate_number = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.Text, default=date.today().strftime("%Y-%m-%d"))
    updated_at = db.Column(db.Text, nullable=True)


class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)


    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.email = kwargs.get('email')
        self.password = bcrypt.hash(kwargs.get('password'))


    def get_token(self, expire_time=24):
        expire_delta = timedelta(hours=expire_time)
        token = create_access_token(
            identity=self.id, expires_delta=expire_delta)
        return token


    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter(cls.email == email).one()
        if not bcrypt.verify(password, user.password):
            raise Exception('No user with this password')
        return user

