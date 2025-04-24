from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

db = SQLAlchemy()

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)
  db.init_app(app)
  CORS(app)

  @app.route('/')
  def home():
    return {'message': 'Backend de LimatchServ funcionando'}
  return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
      db.create_all()
    app.run(debug=True)