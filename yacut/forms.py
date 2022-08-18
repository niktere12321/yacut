from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class URL_mapForm(FlaskForm):
    MAX_LENGTH = 16
    original_link = URLField(
        'Оригинальная длинная сслыка',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(max=MAX_LENGTH), Optional()]
    )
    submit = SubmitField('Создать')
