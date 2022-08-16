from random import choice
from string import ascii_lowercase, ascii_uppercase, digits

from .models import URL_map


def is_unique(custom_id):
    """Проверить короткую ссылку на уникальность."""
    return not URL_map.query.filter_by(short=custom_id).first()


def get_unique_short_id():
    """Сгенерировать короткий идентификатор."""
    letters = ascii_uppercase + ascii_lowercase + digits
    rand_string = ''.join(choice(letters) for i in range(6))
    return rand_string
