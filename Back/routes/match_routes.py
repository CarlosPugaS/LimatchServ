from flask import Blueprint, request, jsonify
from models.entities import db, MatchTrabajo, Presupuesto
from flask_jwt_extended import jwt_required
from datetime import datetime, timezone

match_bp = Blueprint('match', __name__, url_prefix='/api/match')

@match_bp.route('/', methods=['POST'])
@jwt_required
def crear_match(user):
  data = request.get_json()
  presupuesto_id = data.get('presupuesto_id')

  presupuesto = Presupuesto.query.get(presupuesto_id)

  if not presupuesto:
    return jsonify({"message":"presupuesto no encontrado"}), 404
  
  if presupuesto.estado != 'enviado':
    return jsonify({"message":"Presupuesto no ha sido enviado aún"}), 400
  
  if presupuesto.cliente_id != user.id_usuario:
    return jsonify({"message":"No autorizado para aceptar este presupuesto"})
  
  if MatchTrabajo.query.filter_by(presupuesto_id=presupuesto_id).first():
    return jsonify({"message":"Este presupuesto ya tiene un match asociado"})
  
  nuevo_match = MatchTrabajo(
    presupuesto_id=presupuesto_id,
    fecha_aceptacion=datetime.now(timezone.utc),
    estado='en_ejecicion'
  )
  presupuesto.estado = 'aceptado'

  db.session.add(nuevo_match)
  db.session.commit()

  return jsonify({"message":"Match creado exitosamente"}), 201