from flask import Blueprint, request, jsonify
from models.entities import db, Resena, MatchTrabajo
from utils.jwt_utils import jwt_required
from datetime import datetime, timezone 

resenas_bp = Blueprint('resenas', __name__, url_prefix= '/api/resenas')

@resenas_bp.route('/', methods=['POST'])
@jwt_required
def crear_resena(user):
  data = request.get_json()

  match_id = data.get('match_id')
  prestador_id = data.get('prestador_id')
  puntuacion = data.get('puntuacion')
  comentario = data.get('comentario')

  match = MatchTrabajo.query.get(match_id)
  if not match:
    return jsonify({"message":"Match no encontrado"}), 404
  
  if match.estado != "en_ejecucion" or match.presupuesto.cliente_id != user.id_usuario:
    return jsonify({"message":"No autorizado para calificar"}), 403
  
  nueva_resena = Resena(
    match_id= match_id,
    cliente_id= user.id_usuario,
    prestador_id= prestador_id,
    puntuacion= puntuacion,
    comentario= comentario,
    fecha=datetime.now(timezone.utc)
  )
  db.session.add(nueva_resena)
  db.session.commit()

  return jsonify({"message":"Reseña creada exitosamente"}), 201

@resenas_bp.route('/',methods=['GET'])
def obtener_resenas():
  prestador_id = request.args.get('prestador_id', type=int)

  if not prestador_id:
    return jsonify({"message":"Falta parametro 'prestador_id'"}),400
  resenas = resenas.query.filter_by(prestador_id=prestador_id).all()

  resultado = [{
    "id_resena": r.id_resena,
    "cliente_id": r.cliente_id,
    "puntuacion": r.puntuacion,
    "comentario": r.comentario,
    "fecha": r.fecha.strftime("%Y-%m-%d %H:%M:%S")
  } for r in resenas
  ]

  return jsonify(resultado), 200 
