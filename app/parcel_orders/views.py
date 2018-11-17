from flask import jsonify, make_response
from .models import Order
from flask import request
import flask.views
from flask_jwt_extended import jwt_required, get_jwt_identity


class ParcelOrder(flask.views.MethodView):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        if current_user['username'] == "admin":
            orders = Order.order_history()
            if not orders:
                return {"msg": "You have not orderd for any food so you have no order history"}, 200
            return make_response(jsonify({"Parcel orders": orders}), 200)
        else:
            return make_response(jsonify({"message": "You are not authorised to access this resource"}), 401)

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        """ Receiving request data from users"""
        parser = request.get_json()
        parcel_name = parser.get('parcel_name')
        destination = parser.get('destination')
        receiver_name = parser.get('receiver')

        # if not args['food_name']:
        #     return {"message": "Add food_name"}, 400
        #
        # if args['location'] == "":
        #     return {"message": "Add location"}, 400
        # if ' ' in args['food_name']:
        #     return {'message': 'Please avoid adding spaces'}, 400
        #
        # if ' ' in args['location']:
        #     return {'message': 'Please avoid adding spaces'}, 400
        #
        # if not re.compile('^[a-zA-Z]+$').match(args['food_name']):
        #     return {'message': 'food_name should be in characters'}, 400
        #
        # if not re.compile('^[a-zA-Z]+$').match(args['location']):
        #     return {'message': 'location should be in characters'}, 400
        #
        # if len(str(args['food_name'])) < 4:
        #     return {'message': 'food_name should be more than 4 characters'}, 400
        status = "pending"
        present_location = "Headquaters"
        deliver_status = "pending"
        user_id = current_user["user_id"]

        """creating an insatnce of an order class"""
        order = Order(order_id=None, user_id=user_id, parcel_name=parcel_name, receiver_name=receiver_name, \
                      destination=destination, status=status, present_location=present_location,
                      deliver_status=deliver_status)
        select_order = order.fetch_parcel_name()
        if select_order:
            return make_response(jsonify({'message': 'Order has already been placed'}), 403)
        create_order = order.insert_order_data()
        if create_order:
            return make_response(jsonify({'messege': "you have succesfully placed order"}), 201)
        return make_response(jsonify({"message": "Order not placed succesfully"}), 400)


class UserSpecificOrder(flask.views.MethodView):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        user_id = current_user['user_id']
        new_order = Order(user_id=user_id, parcel_name=None, order_id=None, receiver_name=None, status=None,
                          deliver_status=None \
                          , destination=None, present_location=None)
        order = new_order.single_order()
        if not order:
            return make_response(jsonify({'messege': "you have no orders at this time"}), 404)
        return make_response(jsonify({'orders': order}), 200)

    @jwt_required
    def put(self, parcel_id):
        current_user = get_jwt_identity()
        user_id = current_user['user_id']
        parser = request.get_json()
        destination = parser.get('destination')
        order = Order(user_id=user_id, parcel_name=None, order_id=parcel_id, receiver_name=None, status=None,
                      deliver_status=None \
                      , destination=destination, present_location=None)
        if not destination:
            return make_response(jsonify({"message": "Please add a status"}), 400)

        if destination.isspace():
            return make_response(jsonify({'message': 'Please avoid adding spaces'}), 400)

        update_destination = order.update_destination()
        if update_destination:
            return make_response(jsonify({'message': 'destination updated succesfully'}), 201)
        return make_response(jsonify({'message': 'Failed to update destination'}), 400)


class AdminOrderView(flask.views.MethodView):
    @jwt_required
    def put(self, parcel_id):
        current_user = get_jwt_identity()
        if current_user['username'] == "admin":
            parser = request.get_json()
            deliver_status = parser.get('delivery_status')
            order = Order(user_id=None, parcel_name=None, order_id=parcel_id, receiver_name=None, status=None,
                          deliver_status=deliver_status \
                          , destination=None, present_location=None)
            if not deliver_status:
                return make_response(jsonify({"message": "Please add a status"}), 400)

            if deliver_status.isspace():
                return make_response(jsonify({'message': 'Please avoid adding spaces'}), 400)

            update_status = order.update_delivery_status()
            if update_status:
                return make_response(jsonify({'message': 'destination updated succesfully'}), 201)
            return make_response(jsonify({'message': 'Failed to update destination'}), 400)
        return make_response(jsonify({"message": "You are not authorised to access this resource"}), 401)

    @jwt_required
    def put(self, parcel_id):
        current_user = get_jwt_identity()
        if current_user['username'] == "admin":
            parser = request.get_json()
            present_location = parser.get('present_location')
            order = Order(user_id=None, parcel_name=None, order_id=parcel_id, receiver_name=None, status=None,
                          deliver_status=None \
                          , destination=None, present_location=present_location)
            if not present_location:
                return make_response(jsonify({"message": "Please add the present location of the parcel"}), 400)

            if present_location.isspace():
                return make_response(jsonify({'message': 'Please avoid adding spaces'}), 400)

            update_present_location = order.update_present_location()
            if update_present_location:
                return make_response(jsonify({'message': 'present location updated succesfully'}), 201)
            return make_response(jsonify({'message': 'Failed to update present location'}), 400)
        return make_response(jsonify({"message": "You are not authorised to access this resource"}), 401)
