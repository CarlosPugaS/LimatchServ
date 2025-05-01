from flask import Blueprint,request, jsonify 
from models.entities import db, Presupuesto, Usuario
from datetime import datetime, timezone

presupuestos_bp = Blueprint('presupuestos', __name__, url_prefix='/api/presupuestos')

@presupuestos_bp.route('/', methods=['POST'])
def solicitud_presupuesto():
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
def enviar_presupuesto(id):
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


