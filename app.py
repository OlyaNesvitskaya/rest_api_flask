import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required
from config import Config
import logging
from models import *
from schemas import DriverSchema, VehicleSchema, ValidationError, UserSchema
app = Flask(__name__)
app.config.from_object(Config)


engine = db.create_engine("sqlite:///db_for_rest_api.db")
session = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))
Base = declarative_base()
Base.query = session.query_property()

Base.metadata.create_all(engine)


jwt = JWTManager(app)
client = app.test_client()


@app.route('/drivers/driver', methods=['GET'])
@jwt_required()
def get_drivers():
    drivers = session.query(Driver).all()
    schema = DriverSchema(many=True)
    return jsonify(schema.dump(drivers))


@app.route('/drivers/driver/<driver_id>', methods=['GET'])
@jwt_required()
def get_driver(driver_id):
    driver = session.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        return {'message': 'No driver with this id'}, 400
    schema = DriverSchema()
    return jsonify(schema.dump(driver))


@app.route('/drivers/driver', methods=['POST'])
@jwt_required()
def add_driver():
    json_data = request.get_json()
    try:
        data = DriverSchema().load(json_data, unknown="EXCLUDE")
    except ValidationError as err:
        return err.messages, 422
    is_exist_driver = session.query(Driver).filter(Driver.first_name == data['first_name'],
                                                   Driver.last_name == data['last_name']).first()
    if is_exist_driver:
        schema = DriverSchema()
        return jsonify({'message': 'This user already exists'}, schema.dump(is_exist_driver))
    else:
        driver = Driver(**data)
        session.add(driver)
        session.commit()
        return {'message': 'New driver added successfully.'}


@app.route('/drivers/driver/<driver_id>', methods=['PUT'])
@jwt_required()
def update_driver(driver_id):
    json_data = request.get_json()
    item = session.query(Driver).filter(Driver.id == driver_id).first()
    if not item:
        return {'message': 'No driver with this id'}, 400
    try:
        data = DriverSchema().load(json_data, unknown="EXCLUDE", partial=True)
        for key, value in data.items():
            setattr(item, key, value)
        item.updated_at = date.today().strftime("%Y-%m-%d")
        session.commit()
        schema = DriverSchema()
        return jsonify(schema.dump(item))
    except ValidationError as err:
        return err.messages, 422


@app.route('/drivers/driver/<driver_id>', methods=['DELETE'])
@jwt_required()
def delete_driver(driver_id):
    item = session.query(Driver).filter(Driver.id == driver_id).first()
    if not item:
        return {'message': 'No driver with this id'}, 400
    session.delete(item)
    session.commit()
    return {'message': 'Driver deleted successfully'}


@app.route('/vehicles/vehicle', methods=['GET'])
@jwt_required()
def get_vehicles():
    vehicles = session.query(Vehicle).all()
    schema = VehicleSchema(many=True)
    return jsonify(schema.dump(vehicles))


@app.route('/vehicles/vehicle/', methods=['GET'])
@jwt_required()
def get_vehicle_with_drivers_or_not():
    is_with_driver = request.args.get('with_drivers')
    if is_with_driver == 'no':
        vehicles = session.query(Vehicle).filter(Vehicle.driver_id.is_(None))
    else:
        vehicles = session.query(Vehicle).filter(Vehicle.driver_id.is_not(None))
    schema = VehicleSchema(many=True)
    return jsonify(schema.dump(vehicles))


@app.route('/vehicles/vehicle/<vehicle_id>', methods=['GET'])
@jwt_required()
def get_vehicle(vehicle_id):
    vehicle = session.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        return {'message': 'No vehicle with this id'}, 400
    schema = VehicleSchema()
    return jsonify(schema.dump(vehicle))


@app.route('/vehicles/vehicle', methods=['POST'])
@jwt_required()
def add_vehicle():
    json_data = request.get_json()
    try:
        data = VehicleSchema().load(json_data)
    except ValidationError as err:
        return err.messages, 422
    is_exist_vehicle = session.query(Vehicle).filter(Vehicle.make == data['make'],
                                                     Vehicle.model == data['model'],
                                                     Vehicle.plate_number == data['plate_number']).first()
    if is_exist_vehicle:
        schema = VehicleSchema()
        return jsonify({'message': 'This vehicle already exists'}, schema.dump(is_exist_vehicle))
    else:
        vehicle = Vehicle(**data)
        session.add(vehicle)
        session.commit()
        return {'message': 'New vehicle added successfully.'}


@app.route('/vehicles/set_driver/<vehicle_id>', methods=['POST'])
@jwt_required()
def set_driver(vehicle_id):
    driver = request.args.get('set_driver')
    vehicle = session.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if driver == 'yes':
        if vehicle.driver_id:
            return {'message': 'This car is unavailable now.'}
        else:
            json_data = request.get_json()
            try:
                data = VehicleSchema().load(json_data, unknown="EXCLUDE", partial=True)
            except ValidationError as err:
                return err.messages, 422
            vehicle.driver_id = data['driver_id']
            vehicle.updated_at = date.today().strftime("%Y-%m-%d")
            session.commit()
            return {'message': 'Driver added successfully.'}
    else:
        vehicle.driver_id = None
        session.commit()
        return {'message': 'Driver deleted successfully.'}


@app.route('/vehicles/vehicle/<vehicle_id>', methods=['PUT'])
@jwt_required()
def update_vehicle(vehicle_id):
    params = request.json
    item = session.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not item:
        return {'message': 'No vehicle with this id'}, 400
    try:
        data = VehicleSchema().load(params, unknown="EXCLUDE", partial=True)
        for key, value in data.items():
            setattr(item, key, value)
        item.updated_at = date.today().strftime("%Y-%m-%d")
        session.commit()
        schema = VehicleSchema()
        return jsonify(schema.dump(item))
    except ValidationError as err:
        return err.messages, 422


@app.route('/vehicles/vehicle/<vehicle_id>', methods=['DELETE'])
@jwt_required()
def delete_vehicle(vehicle_id):
    item = session.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not item:
        return {'message': 'No vehicle with this id'}, 400
    session.delete(item)
    session.commit()
    return {'message': 'Vehicle deleted successfully'}


@app.route('/register', methods=['POST'])
def register():
    json_data = request.get_json()
    try:
        data = UserSchema().load(json_data)
    except ValidationError as err:
        return err.messages, 422
    user = User(**data)
    session.add(user)
    session.commit()
    return {'message': 'Registration completed successfully'}


@app.route('/login', methods=['POST'])
def login():
    json_data = request.get_json()
    try:
        data = UserSchema(only=('email', 'password')).load(json_data)
    except ValidationError as err:
        return err.messages, 422
    user = User.authenticate(**data)
    token = user.get_token()
    return {'access_token': token}


@app.teardown_appcontext
def shut_down_session(exception=None):
    session.remove()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
