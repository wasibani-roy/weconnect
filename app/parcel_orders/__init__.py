from flask import Blueprint

from .views import ParcelOrder, UserSpecificOrder

orders = Blueprint('parcel_orders', __name__, url_prefix='/api/v2')

orders.add_url_rule('/parcels', view_func=ParcelOrder.as_view('make order'),
                    methods=['POST'], strict_slashes=False)
orders.add_url_rule('/parcels', view_func=ParcelOrder.as_view('get order'),
                    methods=['GET'], strict_slashes=False)
orders.add_url_rule('/parcels/user', view_func=UserSpecificOrder.as_view('view order'),
                    methods=['GET'], strict_slashes=False)
orders.add_url_rule('/parcels/<int:parcel_id>/destination', view_func=UserSpecificOrder.as_view('change destination'),
                    methods=['PUT'], strict_slashes=False)
orders.add_url_rule('/parcels/<int:parcel_id>/status', view_func=UserSpecificOrder.as_view('update product status'),
                    methods=['PUT'], strict_slashes=False)
# orders.add_url_rule('/parcels/<int: parcel_id>/status', view_func=Login.as_view('update present location'),
#                     methods=['POST'], strict_slashes=False)

