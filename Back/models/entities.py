from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from enum import Enum
from models.mixins import TimeStampMixin
from sqlalchemy.schema import CheckConstraint

db = SQLAlchemy()

class EstadoPresupuesto(Enum):
    PENDIENTE = 'pendiente'
    ACEPTADO = 'aceptado'
    RECHAZADO = 'rechazado'
    EN_EJECUCION = 'en_ejecucion'
    FINALIZADO = 'finalizado'

class Rol(db.Model):
    __tablename__ = 'rol'
    id_rol = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)

class Usuario(db.Model, TimeStampMixin):
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(50), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    rut= db.Column(db.String(12), unique=True, nullable=False)
    email = db.Column(db.String(70), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    instagram_url = db.Column(db.String(100))
    facebook_url = db.Column(db.String(100))
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id_rol'), nullable=False)
    rol = db.relationship('Rol', backref='usuarios', lazy=True)

    presupuestos_como_cliente = db.relationship('Presupuesto', foreign_keys='Presupuesto.cliente_id', backref='cliente', lazy=True)
    presupuestos_como_prestadore = db.relationship('Presupuesto', foreign_keys='Presupuesto.prestador_id', backref='prestador', lazy=True)

class Presupuesto(db.Model, TimeStampMixin):
    __tablename__ = 'presupuesto'
    id_presupuesto = db.Column(db.Integer, primary_key=True)
    prestador_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    descripcion_solicitud = db.Column(db.Text, nullable=False)
    descripcion_respuesta = db.Column(db.Text, nullable=True)
    monto = db.Column(db.Numeric(10, 2), nullable=True)
    estado = db.Column(db.String(20), default=EstadoPresupuesto.PENDIENTE.value)


class MatchTrabajo(db.Model, TimeStampMixin):
    __tablename__ = 'match_trabajo'
    id_match = db.Column(db.Integer, primary_key=True)
    presupuesto_id = db.Column(db.Integer, db.ForeignKey('presupuesto.id_presupuesto'), nullable=False, unique=True)
    estado = db.Column(db.String(20), default=EstadoPresupuesto.EN_EJECUCION.value)
    resena = db.relationship('Resena', backref='match', uselist=False, lazy=True)
    calificaciones = db.relationship('Calificacion', backref='match', lazy=True)
    presupuesto = db.relationship('Presupuesto', backref=db.backref('match', uselist=False, lazy=True))

class Resena(db.Model, TimeStampMixin):
    __tablename__ = 'resena'
    id_resena = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match_trabajo.id_match'), nullable=False, unique=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    prestador_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    comentario = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Reseña del cliente {self.cliente_id} para el prestador {self.prestador_id}>'
    

class Calificacion(db.Model, TimeStampMixin):
    __tablename__ = 'calificacion'
    id_calificacion = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match_trabajo.id_match'), nullable=False, unique=True)
    autor_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    receptor_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    puntuacion = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        CheckConstraint('puntuacion >= 1 AND puntuacion <= 5', name='Verifica_puntuación'),
        db.UniqueConstraint('match_id', 'autor_id', name='calificacion_unica')
    )

    def __repr__(self):
        return f'<Calificación de {self.autor_id} a {self.receptor_id} con {self.puntuacion} estrellas>'