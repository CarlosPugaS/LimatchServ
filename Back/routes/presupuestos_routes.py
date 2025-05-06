from flask import Blueprint,request, jsonify 
from models.entities import db, Presupuesto, Usuario
from datetime import datetime, timezone
from utils.role_required import role_required
from utils.jwt_utils import jwt_required

presupuestos_bp = Blueprint('presupuestos', __name__, url_prefix='/api/presupuestos')

@presupuestos_bp.route('/', methods=['POST'])
@jwt_required
@role_required("cliente")
def solicitud_presupuesto(user):
  data = request.get_json()
  
  cliente = Usuario.query.get(data.get("cliente_id"))
  prestador = Usuario.query.get(data.get("prestador_id"))

  if not cliente or not prestador:
    return jsonify({"message":"Cliente o prestador no válido"}),400
  
  if cliente.rol_id != 1: 
    return jsonify({"message":"Solicitud invalida"}),403
  
  if prestador.rol_id != 2: 
    return jsonify({"message":"Solicitud invalida"}),403
  
  nuevo_presupuesto = Presupuesto(
    cliente_id= data['cliente_id'],
    prestador_id= data['prestador_id'],
    descripcion_solicitud= data['descripcion_solicitud'],
    fecha_creacion= datetime.now(timezone.utc),
    estado = 'pendiente'
  )

  db.session.add(nuevo_presupuesto)
  db.session.commit()

  return jsonify({"message":"Su presupuesto ha sido solicitado correctamente"}), 201

@presupuestos_bp.route('/<int:id>', methods=['PUT'])
@jwt_required
@role_required("prestador")
def enviar_presupuesto(user, id):
  data = request.get_json()
  presupuesto = Presupuesto.query.get(id)

  if not presupuesto:
    return jsonify({"message":"Presupuesto no encontrado"}), 404
  prestador = Usuario.query.get(presupuesto.prestador_id)
  if prestador.rol_id != 2:
    return jsonify({"message":"Acción no autorizada"}), 403
  
  presupuesto.monto = data['monto']
  presupuesto.descripcion_respuesta = data['descripcion_respuesta']
  presupuesto.estado = 'enviado'

  db.session.commit()

  return jsonify({"message":"Su presupuesto ha sido enviado correctamente"}), 200

@presupuestos_bp.route('/', methods=['GET'])
def listar_presupuestos():
  cliente_id = request.args.get('client_id',type=int)
  prestador_id  = request.args.get('prestador_id',type=int)

  query = Presupuesto.query

  if cliente_id:
    query = query.filter_by(cliente_id=cliente_id)
  if prestador_id:
    query = query.filter_by(prestador_id=prestador_id)
    
  query = query.filter(Presupuesto.estado != 'descargado')

  presupuestos = query.all()
  resultado= []
  for p in presupuestos:
    resultado.append({
      "id_presupuesto": p.id_presupuesto,
      "cliente_id": p.cliente_id,
      "prestador_id": p.prestador_id,
      "descripcion_solicitud": p.descripcion_solicitud,
      "descripcion_respuesta": p.descripcion_respuesta,
      "monto": float(p.monto) if p.monto else None,
      "fecha_creacion": p.fecha_creacion.strftime("%d-%m-%YHora%H:%M:%S"),
      "estado": p.estado
    })
  return jsonify(resultado),200

@presupuestos_bp.route('/<int:id>', methods=['GET'])
def obtener_presupuesto_id(id):
  presupuesto = Presupuesto.query.get(id)
  if not presupuesto:
    return jsonify({"message":"Presupuesto no encontrado"}),404
  return jsonify({
    "id_presupuesto": presupuesto.id_presupuesto,
    "cliente_id": presupuesto.cliente_id,
    "prestador_id": presupuesto.prestador_id,
    "descripcion_solicitud": presupuesto.descripcion_solicitud,
    "descripcion_respuesta": presupuesto.descripcion_respuesta,
    "monto": float(presupuesto.monto) if presupuesto.monto else None,
    "fecha_creacion": presupuesto.fecha_creacion.strftime("%d-%m-%YT%H:%M:%SZ"),
    "estado": presupuesto.estado
  }), 200

@presupuestos_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required
def eliminar_presupuesto(user, id):
  presupuesto = Presupuesto.query.get(id)

  if not presupuesto:
    return jsonify({"message":"Presupuesto no encontrado"}), 404
  
  if user.id_usuario != presupuesto.cliente_id and user.id_usuario != presupuesto.prestador_id:
    return jsonify({"message":"No autorizado para eliminar este presupuesto"}), 403
  
  db.session.delete(presupuesto)
  db.session.commit()
  return jsonify({"message":"Presupuesto eliminado correctamente"}), 200 

@presupuestos_bp.route('/<int:id>/descartar', methods=['PUT'])
@jwt_required
@role_required("prestador")
#Definimos la funcion con user(Usuario autenticado) y id(id del presupuesto)
def descartar_presupuesto(user, id):
  #Definimos la variable presupuesto con el id del presupuesto que buscamos en la base de datos.
  presupuesto = Presupuesto.query.get(id)

  if not presupuesto:
    return jsonify({"message":"Presupuesto no encontrado"}),404
  #Comparamos el id del prestador al que se asigno el presupuesto con el id 
  #del usuario actualmente autenticado ⬇
  if presupuesto.prestador.id != user.id_usuario:
    return jsonify({"message":"No autirzado para descartar este presupuesto"}),403
  #V
  if presupuesto.estado != 'pendiente':
    return jsonify({"message":"Esta presupuesto ya fue procesado"}),400
  
  #Actualizacion del estado del presupuesto a descartado.
  presupuesto.estado = 'descartado'
  db.session.commit()

  return jsonify({"message":"Presupuesto descartado correctamente"}),200