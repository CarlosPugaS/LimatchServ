from flask import jsonify
from functools import wraps

def role_required(nombre_rol):
  def decorator(f):
    @wraps(f)
    def wrapped(user, *args, **kwargs):
      if user.rol.nombre != nombre_rol:
        return jsonify({"message": f"Acceso denegado: se requiere rol'{nombre_rol}'"}),403
      return f(user, *args, **kwargs)
    return wrapped
  return decorator