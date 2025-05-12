from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import bcrypt, db
from datetime import datetime

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
  
  fecha_str = data['fecha_nacimiento']
  fecha_nacimiento = datetime.strptime(fecha_str, "%d-%m-%Y").date()
  
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
    fecha_nacimiento = fecha_nacimiento,
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
  #Se obtiene una lista de instancias del modelo usuario.
  
  resultado = [
    {
      "id_usuario": u.id_usuario,
      "nombres": u.nombres,
      "apellidos": u.apellidos,
      "fecha_nacimiento": u.fecha_nacimiento.strftime("%d-%m-%Y"),
      "rut": u.rut,
      "email": u.email,
      "telefono": u.telefono,
      "instagram_url": u.instagram_url,
      "facebook_url": u.facebook_url,
      "rol": u.rol.nombre
    }
    for u in usuarios
  ]
  # Utilizamos una list comprehsion para convertir los objetos en formato JSON y enviarlos como resultado.
  return jsonify(resultado), 200

@usuario_bp.route('/prestadores', methods=['GET'])
@jwt_required
def listar_prestadores(user):
  prestadores = Usuario.query.filter_by(rol_id=2).all()
  resultado = [
    {
      "id_usuario": u.id_usuario,
      "nombres": u.nombres,
      "apellidos": u.apellidos,
      "fecha_nacimiento": u.fecha_nacimiento.strftime("%d-%m-%Y"),
      "email": u.email,
      "telefono": u.telefono,
      "rol": u.rol_id,
      "rol_nombre": u.rol.nombre
    } 
    for u in prestadores
  ]
  return jsonify(resultado), 200

@usuario_bp.route('/', methods=['PUT'])
@jwt_required
def modificar_usuario(user):
  data = request.get_json()
#Solo el usuario autenticado puede modificar su propio perfil.
  if user.id_usuario != data["id_usuario"]:
    return jsonify({"message": "No autorizado"}), 403
  #Se obtiene el id_usuario desde la BD y se asigna a la variable usuario, luego se valida.
  usuario = Usuario.query.get(data["id_usuario"])
  if not usuario:
    return jsonify({"message": "El usuario no existe"}), 404
  #Validar que el correo no pertenezca a otro usuario
  nuevo_email = Usuario.query.filter(
    Usuario.email == data['email'],
    Usuario.id_usuario != data['id_usuario']
    ).first()
  if nuevo_email:
    return jsonify({"message":"El correo electrónico ya está en uso"}), 400
  #Si se modifica la contraseña se hashea y actualiza. data['password'] verifica que no este vacia
  if 'password' in data and data['password']:
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    usuario.password = hashed_password
  
  fecha_str = data['fecha_nacimiento']
  fecha_nacimiento = datetime.strptime(fecha_str, "%d-%m-%Y").date()

  usuario.nombres = data['nombres']
  usuario.apellidos = data['apellidos']
  usuario.fecha_nacimiento = fecha_nacimiento
  usuario.email = data['email'].lower()
  usuario.telefono = data['telefono']
  usuario.instagram_url=data.get('instagram_url')
  usuario.facebook_url=data.get('facebook_url')
  usuario.rol_id = data['rol_id']

  db.session.commit()
  # Se muestra mensaje de modificacion y el nombre del rol (Cliente o Prestador).
  return jsonify({"message": "Usuario modificado exitosamente",
                  "Rol_name":usuario.rol.nombre}), 200
  
@usuario_bp.route('/<int:id_usuario>', methods=['DELETE'])
@jwt_required
def eliminar_usuario(user, id_usuario):
  # Solo el usuario autenticado puede eliminar su propia cuenta
  if user.id_usuario != id_usuario:
    return jsonify({"message":"No autorizado"}), 403
  #Verificamos la existencia del id_usuario
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
    "fecha_nacimiento": user.fecha_nacimiento.strftime("%d-%m-%Y"),
    "rut": user.rut,
    "email":user.email,
    "telefono": user. telefono,
    "instagram_url": user.instagram_url,
    "facebook_url": user.facebook_url,
    "rol_id": user.rol_id,
    "rol_nombre": user.rol.nombre
  }), 200