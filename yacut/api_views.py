import re
from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URL_map
from .utils import get_unique_short_id, is_unique


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url_map = URL_map.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND.value)
    return jsonify(url=url_map.original), HTTPStatus.OK.value


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()
    validate_api_input(data)
    if not data.get('custom_id'):
        data['custom_id'] = get_unique_short_id()
    url_map = URL_map()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED.value


def validate_api_input(data):
    if data is None:
        raise InvalidAPIUsage(
            'Отсутствует тело запроса', HTTPStatus.BAD_REQUEST
        )
    if 'url' not in data:
        raise InvalidAPIUsage(
            '\"url\" является обязательным полем!', HTTPStatus.BAD_REQUEST
        )
    if not re.match(r'^https?://', data['url']):
        raise InvalidAPIUsage(
            'Указан недопустимый url!', HTTPStatus.BAD_REQUEST
        )
    custom_id = data.get('custom_id')
    if not custom_id:
        return
    if not 1 < len(custom_id) < 16:
        raise InvalidAPIUsage(
            'Указано недопустимое имя для короткой ссылки',
            HTTPStatus.BAD_REQUEST
        )
    if not re.match(r'^[a-zA-Z0-9]+$', custom_id):
        raise InvalidAPIUsage(
            'Указано недопустимое имя для короткой ссылки',
            HTTPStatus.BAD_REQUEST
        )
    if not is_unique(custom_id):
        raise InvalidAPIUsage(
            f'Имя "{custom_id}" уже занято.', HTTPStatus.BAD_REQUEST
        )
