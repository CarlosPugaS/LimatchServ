from flask import Flask
from config import Config
from extensions import bcrypt, db, migrate, cors, jwt, ma
from models import *

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)

  db.init_app(app)
  bcrypt.init_app(app)
  migrate.init_app(app, db)
  cors.init_app(app)
  jwt.init_app(app)
  ma.init_app(app)

  
  @app.route('/')
  def home():
    return {'message': 'Backend de LimatchServ funcionando'}
  return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)