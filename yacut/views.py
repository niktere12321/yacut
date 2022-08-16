from flask import flash, redirect, render_template, url_for

from . import app, db
from .forms import URL_mapForm
from .models import URL_map
from .utils import get_unique_short_id, is_unique


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URL_mapForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if custom_id and not is_unique(custom_id):
            flash(f'Имя {custom_id} уже занято!', 'info')
            return render_template('index.html', form=form)
        if not custom_id:
            custom_id = get_unique_short_id()
        while not is_unique(custom_id):
            custom_id = get_unique_short_id()
        url_map = URL_map(
            original=form.original_link.data,
            short=custom_id or get_unique_short_id()
        )
        db.session.add(url_map)
        db.session.commit()
        ref = url_for('redirect_view', custom_id=custom_id, _external=True)
        flash('Ваша новая ссылка готова:', 'info')
        flash(ref, 'ref')
    return render_template('index.html', form=form)


@app.route('/<string:custom_id>')
def redirect_view(custom_id):
    url_map = URL_map.query.filter_by(short=custom_id).first_or_404()
    return redirect(url_map.original)
