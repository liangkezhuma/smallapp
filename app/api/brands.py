from flask import jsonify, request, url_for
from app import db
from app.models import Brands
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request


@bp.route('/brands', methods=['POST'])
# @token_auth.login_required
def create_brand():
    data = request.get_json() or {}
    if 'brand_name' not in data:
        return bad_request('must include brand_name fields')
    if Brands.query.filter_by(brand_name=data['brand_name']).first():
        return bad_request('please use a different brand_name')
    brand = Brands()
    brand.from_dict(data, new_brand=True)
    db.session.add(brand)
    db.session.commit()
    response = jsonify(brand.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for(
        'api.get_brands', id=brand.brand_id)
    return response


@bp.route('/brands', methods=['GET'])
# @token_auth.login_required
def get_brands():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Brands.to_collection_dict(
        Brands.query, page, per_page, 'api.get_brands')
    return jsonify(data)


@bp.route('/brands/<int:brand_id>', methods=['PUT'])
# @token_auth.login_required
def update_brand(brand_id):
    brand = Brands.query.get_or_404(brand_id)
    data = request.get_json() or {}
    if 'brand_name' in data and Brands.query.filter_by(
            brand_name=data['brand_name']).first():
        return bad_request('please use a different brand_name')
    brand.from_dict(data, new_brand=False)
    db.session.commit()
    return jsonify(brand.to_dict())


@bp.route('/brands/<int:brand_id>', methods=['GET'])
# @token_auth.login_required
def get_brand(brand_id):
    return jsonify(Brands.query.get_or_404(brand_id).to_dict())
