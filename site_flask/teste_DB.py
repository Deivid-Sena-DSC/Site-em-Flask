from site_flask import app, database
from site_flask.models import Usuarios

with app.app_context():
    database.drop_all()
    database.create_all()
    database.session.commit()
    database.session.close_all()