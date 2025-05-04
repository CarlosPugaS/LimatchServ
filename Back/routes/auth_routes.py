from flask import Blueprint, request, jsonify
from models.entities import Usuario, db
from flask import current_app
import jwt
from datetime import datetime, timedelta, timezone
from extensions import bcrypt

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/login', methods=['POST'])
def login():
  data = request.get_json()
  email = data.get('email')
  password = data.get('password')

  usuario = Usuario.query.filter_by(email=email).first()
  if not usuario:
    return jsonify({"message": "Usuario no encontrado"}), 404
  
  if not bcrypt.check_password_hash(usuario.password, password):
    return jsonify({"message": "Contraseña incorrecta"}), 401
  
# Creacion de payload para el token JWT
# Se establece el id_usuario y rol_id como parte del payload del token.
  payload = {
    "id_usuario" : usuario.id_usuario,
    'rol_id' : usuario.rol_id,
    'exp': datetime.now(timezone.utc) + timedelta(hours=1)  # El token expirara en 1 hora
  }
# Se establece el token JWT y la clave secreta definida en la configuracion de la aplicacion.
# Se utiliza el algoritmo HS256 para la firma del token.
# Se devuelve el token al cliente en formato JSON.
  print("TOKEN PAYLOAD:", payload)
  
  token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
  return jsonify({"token": token}), 200