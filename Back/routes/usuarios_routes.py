from flask import Blueprint, request, jsonify
from models.entities import Usuario, db
from extensions import bcrypt
from utils.jwt_utils import jwt_required

usuario_bp = Blueprint('usuarios', __name__, url_prefix='/api/usuarios')

@usuario_bp.route('/', methods=['POST'])
def crear_usuario():
  data = request.get_json()
  #Se verifica la existencia del RUT en la BD
  rut_existente = Usuario.query.filter_by(rut= data['rut']).first()
  if rut_existente:
    return jsonify({"message":" El RUT ingresado ya existe"}),400
  #Se verifica el Correo en la BD
  email_existente = Usuario.query.filter_by(email=data['email']).first()
  if email_existente:
    return jsonify({"message":"El correo electronico ya existe"}),400
  
  #Extraemos la password en texto plano, utilizamos bcrypt para encriptarla y codificar el hash
  #Así guardamos la cadena de texto correspondiente al password procesada en nuestra BD
  password = data['password']
  hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
  #Creamos un nuevo objeto Usuario usando los datos obtenidos.
  #Convertimos email en minúsculas 
  #Las RRSS se obtienen con .get (Si no estan presentes, el campo queda vacio '')
  #password guarda el hashed_password 
  nuevo_usuario = Usuario(
    nombres=data['nombres'],
    apellidos=data['apellidos'],
    rut=data['rut'],
    email=data['email'].lower(),
    password = hashed_password,
    telefono=data['telefono'],
    instagram_url=data.get('instagram_url', ''),
    facebook_url=data.get('facebook_url', ''),
    rol_id=data['rol_id']
  )
  # Añadimos el nuevo objeto a la sesion actual de la BD
  db.session.add(nuevo_usuario)
  # Se confirma el cambio,se guarda en la BD y se envia el mensaje
  db.session.commit()
  return jsonify({"message": "Usuario creado exitosamente"}),201

@usuario_bp.route('/', methods=['GET'])
@jwt_required 
def listar_usuarios(user):
  #El párametro user es el usuario autenticado, se obtiene desde el token JWT
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
      "rol": u.rol.nombre
    }
    for u in usuarios
  ]
  return jsonify(resultado), 200

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

@usuario_bp.route('mi-perfil', methods=['GET'])
@jwt_required
def mi_perfil(user):
  return jsonify({
    "id_usuario": user.id_usuario,
    "nombres": user.nombres,
    "apellidos": user.apellidos,
    "rut": user.rut,
    "email":user.email,
    "telefono": user. telefono,
    "instagram_url": user.instagram_url,
    "facebook_url": user.facebook_url,
    "rol_id": user.rol_id,
    "rol_nombre": user.rol.nombre
  }), 200