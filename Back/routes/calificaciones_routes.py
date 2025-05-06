from flask import Blueprint, request, jsonify
from models.entities import db, CalificacionCliente, MatchTrabajo
from utils.jwt_utils import jwt_required
from utils.role_required import role_required
from datetime import datetime, timezone

calificaciones_bp = Blueprint('calificaciones', __name__, url_prefix='/api/calificaciones')

@calificaciones_bp.route('/', methods=['POST'])
@jwt_required
@role_required("prestador")
def crear_calificacion(user):
  data = request.get_json()

  match_id = data.get('match_id')
  cliente_id = data.get('cliente_id')
  puntuacion = data.get('puntuacion')
  comentario = data.get('comentario')

  match = MatchTrabajo.query.get(match_id)
  if not match:
    return jsonify({"message":"Match no encontrado"}), 404
  
  if match.prespuesto.prestador_id != user.id_usuario:
    return jsonify({"message":"No autorizado para calificar"}), 403
  
  nueva_calificacion = CalificacionCliente(
    match_id= match_id,
    prestador_id= user.id_usuario,
    cliente_id= cliente_id,
    puntuacion= puntuacion,
    comentario= comentario,
    fecha=datetime.now(timezone.utc)
  )
  db.session.add(nueva_calificacion)
  db.session.commit()
  return jsonify({"message": "calificación creada exitosamente"}), 201

@calificaciones_bp.route('/', methods=['GET'])
def obtener_calificaciones():
  cliente_id = request.args.get('cliente_id', type=int)

  if not cliente_id:
    return jsonify({"message":"Falta el parámetro 'cliente_id'"}),400
  calificaciones = CalificacionCliente.query.filter_by(cliente_id=cliente_id).all()

  resultado= [{
    "id_calificacion": c.id_calificacion,
    "prestador_id":c.prestador_id,
    "puntuacion": c.puntuacion,
    "comentario": c.comentario,
    "fecha": c.fecha.strftime("%Y-%m-%d %H:%M:%S")
  } for c in calificaciones
  ]
  return jsonify(resultado), 200