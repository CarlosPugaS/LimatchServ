from flask import Flask
from config import Config
from routes.usuarios_routes import usuario_bp
from routes.roles_routes import roles_bp
from routes.presupuestos_routes import presupuestos_bp
from routes.auth_routes import auth_bp
from routes.resenas_routes import resenas_bp
from routes.calificaciones_routes import calificaciones_bp
from routes.match_routes import match_bp
from extensions import bcrypt, db, migrate, cors, jwt

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)

  db.init_app(app)
  bcrypt.init_app(app)
  migrate.init_app(app, db)
  cors.init_app(app)
  jwt.init_app(app)

  
  app.register_blueprint(auth_bp)
  app.register_blueprint(usuario_bp)
  app.register_blueprint(roles_bp)
  app.register_blueprint(presupuestos_bp)
  app.register_blueprint(resenas_bp)
  app.register_blueprint(calificaciones_bp)
  app.register_blueprint(match_bp)
  
  @app.route('/')
  def home():
    return {'message': 'Backend de LimatchServ funcionando'}
  return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)