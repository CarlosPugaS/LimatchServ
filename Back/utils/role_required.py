from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from models.entities import Usuario
from functools import wraps

# Decorador para verificar el rol del usuario. 
def jwt_required_role(f):
  @wraps(f)
  #wraps para guardar la data de la funcion original.
  @jwt_required()
  def decorated_function(*args, **kwargs):
    # Se obtiene el id del usuario autenticado a partir del token JWT.
    user_id = get_jwt_identity()
    user = Usuario.query.get(user_id)
    if not user:
      return jsonify({"message": "Usuario no encontrado"}), 404
    # si el ususario no tiene el rol requerido, se devuelve un 404.
    return f(user, *args, **kwargs)
  return decorated_function

def generate_token(user):
  # Genera un nuevo token JWT para el usuario autenticado.
  access_token = create_access_token(identity=user.id_usuario, additional_claims={"rol": user.rol.nombre, "email": user.email})
  return access_token
# Se obtiene el rol del usuario autenticado a partir del token JWT.