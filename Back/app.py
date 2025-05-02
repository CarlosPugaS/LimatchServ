from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
from flask_migrate import Migrate
from models.entities import db
from routes.usuarios_routes import usuario_bp
from routes.roles_routes import roles_bp
from routes.presupuestos_routes import presupuestos_bp
from routes.auth_routes import auth_bp
from extensions import bcrypt

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)

  db.init_app(app)
  bcrypt.init_app(app)

  migrate = Migrate(app, db)
  CORS(app)

  app.register_blueprint(auth_bp)
  app.register_blueprint(usuario_bp)
  app.register_blueprint(roles_bp)
  app.register_blueprint(presupuestos_bp)

  @app.route('/')
  def home():
    return {'message': 'Backend de LimatchServ funcionando'}
  return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)