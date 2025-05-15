from datetime import timedelta
from flask import Blueprint, request, jsonify
from models.entities import Usuario
from extensions import db, bcrypt
from schemas.usuario_schema import UsuarioRegistroSchema, UsuarioEdicionSchema, perfil_privado_schema, perfil_publico_schema
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy import or_

usuario_bp = Blueprint('usuario', __name__, url_prefix='/api/usuarios')


@usuario_bp.route('/', methods=['POST'])
def registrar_usuario():
    data = request.get_json()
    schema = UsuarioRegistroSchema()
    try:
        datos_validados = schema.load(data)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    rut = datos_validados['rut'].lower()
    if Usuario.query.filter_by(rut=rut).first:
        return jsonify({"error": "El RUT ya está registrado"}), 400
    email = datos_validados['email'].lower()
    if Usuario.query.filter_by(email=email).first():
        return jsonify({"error": "El correo ya está registrado"}), 400
    hashed_password = bcrypt.generate_password_hash(datos_validados['password']).decode('utf-8')
    nuevo_usuario = Usuario(
        nombres=datos_validados['nombres'],
        apellidos=datos_validados['apellidos'],
        fecha_nacimiento=datos_validados['fecha_nacimiento'],
        rut=rut,
        email=email,
        password=hashed_password,
        telefono=datos_validados['telefono'],
        instagram_url=datos_validados.get('instagram_url', ''),
        facebook_url=datos_validados.get('facebook_url', ''),
        rol_id=datos_validados.get('rol_id'),
        foto_url=datos_validados.get('foto_url', ''),
        descripcion=datos_validados.get('descripcion', ''),
        direccion=datos_validados.get('direccion', ''),
        web_url=datos_validados.get('web_url', '')
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    access_token = create_access_token(identity=nuevo_usuario.id, expires_delta=timedelta(days=1))
    return jsonify({"message": "Usuario creado exitosamente",
                    "access_token": access_token}), 201


@usuario_bp.route('/perfil', methods=['GET'])
@jwt_required()
def obtener_perfil():
    id_usuario_actual = get_jwt_identity()
    usuario = Usuario.query.get(id_usuario_actual)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return perfil_privado_schema.jsonify(usuario), 200


@usuario_bp.route('<int:id>', methods=['GET'])
def obtener_perfil_publico(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return perfil_publico_schema.jsonify(usuario), 200


@usuario_bp.route('/publicos', methods=['GET'])
def listar_perfiles_publicos():
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)
    busqueda = request.args.get('q', '', type=str).lower()
    rol_id = request.args.get('rol_id', type=int)

    query = Usuario.query
    if busqueda:
        query = query.filter(or_(Usuario.nombres.ilike(f'%{busqueda}%'), Usuario.apellidos.ilike(f'%{busqueda}%')))
    if rol_id:
        query = query.filter_by(rol_id=rol_id)
    total = query.count()
    usuarios = query.offset(offset).limit(limit).all()
    usuarios_serializados = perfil_publico_schema.dump(usuarios, many=True)
    return jsonify({"resultados": usuarios_serializados,
                    "total": total,
                    "limit": limit,
                    "offset": offset}), 200


@usuario_bp.route('/perfil', methods=['PUT'])
@jwt_required
def actualizar_perfil():
    id_usuario_actual = get_jwt_identity()
    usuario = Usuario.query.get(id_usuario_actual)

    if not usuario:
        return ({"message": "Usuario no encontrado"}), 404

    data = request.get_json()
    schema = UsuarioEdicionSchema()

    try:
        datos_validados = schema.load(data)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    for campo, valor in datos_validados.items():
        setattr(usuario, campo, valor)
    db.session.commit()
    return perfil_privado_schema.jsonify(usuario), 200


@usuario_bp.route('/perfil', methods=['DELETE'])
@jwt_required
def eliminar_pefil():
    id_usuario = get_jwt_identity()
    usuario = Usuario.query.get(id_usuario)

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    db.session.delete(usuario)
    db.session.commit()

    return jsonify({"message": "Cuenta eliminada exitosamente"}), 200
