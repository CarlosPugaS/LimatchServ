from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class Rol(db.Model):
    __tablename__ = 'rol'
    id_rol = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.Text, nullable=False)
    telefono = db.Column(db.String(20))
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id_rol'), nullable=False)

class CategoriaServicio(db.Model):
    __tablename__ = 'categoria_servicio'
    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.Text)

class EspecialidadPrestador(db.Model):
    __tablename__ = 'especialidad_prestador'
    id_especialidad = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria_servicio.id_categoria'), nullable=False)

class Presupuesto(db.Model):
    __tablename__ = 'presupuesto'
    id_presupuesto = db.Column(db.Integer, primary_key=True)
    prestador_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    estado = db.Column(db.String(20), default='pendiente')

class MatchTrabajo(db.Model):
    __tablename__ = 'match_trabajo'
    id_match = db.Column(db.Integer, primary_key=True)
    presupuesto_id = db.Column(db.Integer, db.ForeignKey('presupuesto.id_presupuesto'), nullable=False, unique=True)
    fecha_aceptacion = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    estado = db.Column(db.String(20), default='en_ejecucion')

class Resena(db.Model):
    __tablename__ = 'resena'
    id_resena = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match_trabajo.id_match'), nullable=False, unique=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    prestador_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    puntuacion = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text)
    fecha = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class CalificacionCliente(db.Model):
    __tablename__ = 'calificacion_cliente'
    id_calificacion = db.Column(db.Integer, primary_key=True)
    prestador_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    puntuacion = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text)
    fecha = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
