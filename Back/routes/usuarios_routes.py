from flask import Blueprint, request, jsonify
from models.entities import Usuario, db

usuario_bp = Blueprint('usuarios', __name__, url_prefix='/api/usuarios')

@usuario_bp.route('/', methods=['GET'])
def listar_usuarios():
  usuarios = Usuario.query.all()
  resultado = [
    {
      "id_usuario": u.id_usuario,
      "nombres": u.nombres,
      "apellidos": u.apellidos,
      "rut": u.rut,
      "email": u.email,
      "telefono": u.telefono,
      "instagram_url": u.instagram_url,
      "facebook_url": u.facebook_url,
      "rol": u.rol_id,
    }
    for u in usuarios
  ]
  return jsonify(resultado), 200

@usuario_bp.route('/', methods=['POST'])
def crear_usuario():
  data = request.get_json()
  # validando RUT
  rut_existente = Usuario.query.filter_by(rut=data['rut']).first()
  if rut_existente:
    return jsonify({"message":" El RUT ingresado ya posee una cuenta activa"}),400
  # Validando Correo electronico
  email_existente = Usuario.query.filter_by(email=data['email']).first()
  if email_existente:
    return jsonify({"message":"El correo electronico ya existe"}),400
  
  nuevo_usuario = Usuario(
    nombres=data['nombres'],
    apellidos=data['apellidos'],
    rut=data['rut'],
    email=data['email'].lower(),
    password=data['password'],
    telefono=data['telefono'],
    instagram_url=data.get('instagram_url', ''),
    facebook_url=data.get('facebook_url', ''),
    rol_id=data['rol_id']
  )
  db.session.add(nuevo_usuario)
  db.session.commit()
  return jsonify({"message": "Usuario creado exitosamente"}),201

@usuario_bp.route('/', methods=['PUT'])
def modificar_usuario():
  data = request.get_json()
  usuario = Usuario.query.get(data["id_usuario"])
  if not usuario:
    return jsonify({"message": "El usuario no existe"}), 404
  usuario.nombres = data['nombres']
  usuario.apellidos = data['apellidos']
  usuario.email = data['email']
  usuario.password = data['password']
  usuario.telefono = data['telefono']
  usuario.instagram_url=data.get('instagram_url')
  usuario.facebook_url=data.get('facebook_url')
  usuario.rol_id = data['rol_id']
  db.session.commit()
  return jsonify({"message": "Usuario modificado exitosamente"}), 200
  
@usuario_bp.route('/<int:id_usuario>', methods=['DELETE'])
def eliminar_usuario(id_usuario):
  usuario = Usuario.query.get(id_usuario)
  if not usuario :
    return jsonify({"message" : "El usuario no existe"}), 404
  db.session.delete(usuario)
  db.session.commit()
  return jsonify({"message" : "Usuario eliminado correctamente"}), 200