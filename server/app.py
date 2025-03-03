from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_login import LoginManager
from models import db
from routes import checkout, checkin, active_racers, trail_status, register, login, logout

# Initialize Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/race_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database & Migrations
db.init_app(app)
migrate = Migrate(app, db)

# Initialize SocketIO & Login Manager
socketio = SocketIO(app, cors_allowed_origins="*")
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Register Routes
from routes import routes
app.register_blueprint(routes)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
