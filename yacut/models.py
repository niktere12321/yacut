from datetime import datetime

from flask import url_for

from yacut import db


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                'redirect_view', custom_id=self.short, _external=True
            ),
        )

    def from_dict(self, data):
        field_map = {
            'url': 'original',
            'custom_id': 'short'
        }
        for field in field_map:
            if field in data:
                setattr(self, field_map[field], data[field])
