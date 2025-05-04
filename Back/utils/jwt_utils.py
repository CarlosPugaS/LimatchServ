from flask import request, current_app, jsonify
from models.entities import Usuario
from functools import wraps
import jwt

def get_current_user():
  auth_header = request.headers.get('Authorization')

  if not auth_header or not auth_header.startswith("Bearer "):
    return jsonify({"message":"Token no proporcionado"}), 401
  
  try: 
    token = auth_header.split(" ")[1]
    payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    user_id = payload.get("id_usuario")

    if not user_id:
      return jsonify({"message": "Token invalido"}), 401
    
    user = Usuario.query.get(user_id)
    if not user:
      return jsonify({"Message":"Usuario no encontrado"}), 404
    
    return user
  except jwt.ExpiredSignatureError:
    return jsonify({"message":"Token expirado"}), 401
  except jwt.InvalidTokenError:
    return jsonify({"message":"Token invalido"}), 401

def jwt_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    user = get_current_user()

    if isinstance(user, tuple):
      return user
    return f(user, *args, **kwargs)
  return decorated_function