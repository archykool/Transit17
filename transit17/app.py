from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from backend.config.settings import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from backend.error_handlers import handle_mta_error
from backend.services.mta import MTAServiceFactory

# initialize Flask app
app = Flask(__name__)

# configure database
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

# initialize database
db = SQLAlchemy(app)

# register error handler
app.register_error_handler(Exception, handle_mta_error)

# initialize MTA service factory
mta_factory = MTAServiceFactory()

# import routes
from backend.api.routes import subway, lirr, mnr, alerts

# register blueprints
app.register_blueprint(subway.bp)
app.register_blueprint(lirr.bp)
app.register_blueprint(mnr.bp)
app.register_blueprint(alerts.bp)

if __name__ == '__main__':
    app.run(debug=True) 