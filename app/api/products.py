from flask import jsonify, request, url_for
from app import db
from app.models import Products
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request


@bp.route('/products', methods=['POST'])
# @token_auth.login_required
def create_product():
    data = request.get_json() or {}
    if 'product_name' not in data:
        return bad_request('must include product_name fields')
    if Products.query.filter_by(product_name=data['product_name']).first():
        return bad_request('please use a different product_name')
    product = Products()
    product.from_dict(data, new_product=True)
    db.session.add(product)
    db.session.commit()
    response = jsonify(product.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for(
        'api.get_products', id=product.product_id)
    return response


@bp.route('/products', methods=['GET'])
# @token_auth.login_required
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Products.to_collection_dict(
        Products.query, page, per_page, 'api.get_products')
    return jsonify(data)


@bp.route('/products/<int:product_id>', methods=['PUT'])
# @token_auth.login_required
def update_product(product_id):
    product = Products.query.get_or_404(product_id)
    data = request.get_json() or {}
    if 'product_name' in data and Products.query.filter_by(
            product_name=data['product_name']).first():
        return bad_request('please use a different product_name')
    product.from_dict(data, new_product=False)
    db.session.commit()
    return jsonify(product.to_dict())


@bp.route('/products/<int:product_id>', methods=['GET'])
# @token_auth.login_required
def get_product(product_id):
    return jsonify(Products.query.get_or_404(product_id).to_dict())
