from flask import jsonify, request, url_for
from app import db
from app.models import Orders, Order_items
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request


@bp.route('/orders', methods=['POST'])
# @token_auth.login_required
def create_order():
    data = request.get_json() or {}
    if 'order_items' not in data:
        return bad_request('must include order_items')
    if len(data['order_items']) < 1:
        return bad_request('must include order_items')
    order = Orders()
    order.from_dict(data, new_order=True)
    db.session.add(order)
    # db.session.commit()
    item_id = 1
    for item in data['order_items']:
        order_item = Order_items()
        # order_item.order_id = order.order_id
        order_item.item_id = item_id
        item_id += 1
        order_item.from_dict(item, new_item=True)
        order.order_items.append(order_item)
    db.session.commit()
    response = jsonify(order.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for(
        'api.get_orders', id=order.order_id)
    return response


@bp.route('/orders', methods=['GET'])
# @token_auth.login_required
def get_orders():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Orders.to_collection_dict(
        Orders.query, page, per_page, 'api.get_orders')
    return jsonify(data)


@bp.route('/orders/<int:order_id>', methods=['PUT'])
# @token_auth.login_required
def update_order(order_id):
    order = Orders.query.get_or_404(order_id)
    data = request.get_json() or {}
    if 'order_status' in data:
        order.from_dict(data, new_order=False)
    if 'order_items' in data:
        for item in data['order_items']:
            order_item = Order_items.query.get_or_404(
                (order.order_id, item['item_id']))
            order_item.from_dict(item, new_item=False)
    db.session.commit()
    return jsonify(order.to_dict())


@bp.route('/orders/<int:order_id>', methods=['GET'])
# @token_auth.login_required
def get_order(order_id):
    return jsonify(Orders.query.get_or_404(order_id).to_dict())
