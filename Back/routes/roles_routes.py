from flask import Blueprint, jsonify
from models.entities import Rol

roles_bp = Blueprint('roles', __name__, url_prefix='/api/roles')

@roles_bp.route('/', methods=['GET'])
def listar_roles():
  roles = Rol.query.all()
  resultado = [{"id_rol": r.id_rol, "nombre": r.nombre} for r in roles]
  return jsonify(resultado), 200