from flask import Blueprint, request, jsonify
from models.entities import Usuario
from extensions import db, bcrypt
from schemas.usuario_schema import UsuarioRegistroSchema
from marshmallow import ValidationError

usuario_bp = Blueprint('usuario', __name__, url_prefix='/api/usuarios')

@usuario_bp.route('/crear_usuario', methods=['POST'])
def crear_usuario():
  data = request.get_json()
  schema = UsuarioRegistroSchema()
  try:
    datos_validados = schema.load(data)
  except ValidationError as err:
    return jsonify({"error": err.messages}), 400
  if Usuario.query.filter_by(rut=datos_validados['rut']).first():
    return jsonify({"error": "El RUT ya está registrado"}), 400
  if Usuario.query.filter_by(email=datos_validados['email']).lower().first():
    return jsonify({"error": "El correo ya está registrado"}), 400
  hashed_password = bcrypt.generate_password_hash(datos_validados['password']).decode('utf-8')
  nuevo_usuario = Usuario(
    nombres=datos_validados['nombres'],
    apellidos=datos_validados['apellidos'],
    fecha_nacimiento=datos_validados['fecha_nacimiento'],
    rut=datos_validados['rut'],
    email=datos_validados['email'].lower(),
    password=hashed_password,
    telefono=datos_validados['telefono'],
    instagram_url=datos_validados.get('instagram_url', ''),
    facebook_url=datos_validados.get('facebook_url', ''),
    rol_id=datos_validados.get['rol_id']
  )
  db.session.add(nuevo_usuario)
  db.session.commit()
  return jsonify({"message": "Usuario creado exitosamente"}), 201