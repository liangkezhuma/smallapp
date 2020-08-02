from flask import jsonify, request, url_for
from app import db
from app.models import Categories
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request


@bp.route('/categories', methods=['POST'])
# @token_auth.login_required
def create_category():
    data = request.get_json() or {}
    if 'category_name' not in data:
        return bad_request('must include category_name fields')
    if Categories.query.filter_by(category_name=data['category_name']).first():
        return bad_request('please use a different category_name')
    category = Categories()
    category.from_dict(data, new_category=True)
    db.session.add(category)
    db.session.commit()
    response = jsonify(category.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for(
        'api.get_categories', id=category.category_id)
    return response


@bp.route('/categories', methods=['GET'])
# @token_auth.login_required
def get_categories():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Categories.to_collection_dict(
        Categories.query, page, per_page, 'api.get_categories')
    return jsonify(data)


@bp.route('/categories/<int:category_id>', methods=['PUT'])
# @token_auth.login_required
def update_category(category_id):
    category = Categories.query.get_or_404(category_id)
    data = request.get_json() or {}
    if 'category_name' in data and Categories.query.filter_by(
            category_name=data['category_name']).first():
        return bad_request('please use a different category_name')
    category.from_dict(data, new_category=False)
    db.session.commit()
    return jsonify(category.to_dict())


@bp.route('/categories/<int:category_id>', methods=['GET'])
# @token_auth.login_required
def get_category(category_id):
    return jsonify(Categories.query.get_or_404(category_id).to_dict())
