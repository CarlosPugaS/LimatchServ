from enum import Enum
from utils.mixin import TimeStampMixin
from sqlalchemy.schema import CheckConstraint
from extensions import db


class EstadoPresupuesto(Enum):
    ENVIADO = 'enviado'# Ciente envia la solicitud al prestador
    PENDIENTE = 'pendiente'# Prestador envia el presupuesto al cliente y queda pendiente de aceptación
    RECHAZADO = 'rechazado'# Prestador rechaza la solicitud o cliente rechaza el presupuesto
    EN_EJECUCION = 'en_ejecucion'# cliente acepta el presupuesto y se inicia el trabajo
    FINALIZADO = 'finalizado'# Cliente marca el trabajo como finalizado


class Rol(db.Model):
    __tablename__ = 'rol'
    id_rol = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<Rol {self.nombre}>'


class Usuario(db.Model, TimeStampMixin):
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.Integer, primary_key=True)
    foto_url = db.Column(db.String(100), default='/static/img/defaul_avatar.png', nullable=False)
    nombres = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(50), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    rut = db.Column(db.String(12), unique=True, nullable=False)
    email = db.Column(db.String(70), unique=True, nullable=False)
    descripcion = db.Column(db.String(255), default='')
    password = db.Column(db.Text, nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    instagram_url = db.Column(db.String(100))
    facebook_url = db.Column(db.String(100))
    web_url = db.Column(db.String(100), default='')
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id_rol'), nullable=False)
    rol = db.relationship('Rol', backref='usuarios', lazy=True)

# Relaciones inversas entre presupuestos y los usuarios como cliente y prestador, para retornar los presupuestos asociados a cada usuario.
    presupuestos_como_cliente = db.relationship('Presupuesto', foreign_keys='Presupuesto.cliente_id', backref='cliente', lazy=True)
    presupuestos_como_prestador = db.relationship('Presupuesto', foreign_keys='Presupuesto.prestador_id', backref='prestador', lazy=True)

    def __repr__(self):
        return f'<Usuario {self.nombres} {self.apellidos}>'


class Presupuesto(db.Model, TimeStampMixin):
    __tablename__ = 'presupuesto'
    id_presupuesto = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    prestador_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    servicio_id = db.Column(db.Integer, db.ForeignKey('servicio.id_servicio'), nullable=False)
    descripcion_solicitud = db.Column(db.Text, nullable=False)
    descripcion_respuesta = db.Column(db.Text, nullable=True)
    monto = db.Column(db.Numeric(10, 2), nullable=True)
    estado = db.Column(db.String(20), default=EstadoPresupuesto.ENVIADO.value, nullable=False)
    # El rol de cliente y prestador se definen en la tabla de usuario, por lo tanto no se necesario definirlo aquí.

    def __repr__(self):
        return f'<Presupuesto {self.id_presupuesto} - estado: {self.estado}>'


class MatchTrabajo(db.Model, TimeStampMixin):
    __tablename__ = 'match_trabajo'
    id_match = db.Column(db.Integer, primary_key=True)
    presupuesto_id = db.Column(db.Integer, db.ForeignKey('presupuesto.id_presupuesto'), nullable=False, unique=True)
    estado = db.Column(db.String(20), default=EstadoPresupuesto.EN_EJECUCION.value, nullable=False)
    resena = db.relationship('Resena', backref='match', uselist=False, lazy=True)
    calificaciones = db.relationship('Calificacion', backref='match', lazy=True)
    presupuesto = db.relationship('Presupuesto', backref=db.backref('match', uselist=False, lazy=True))


class Resena(db.Model, TimeStampMixin):
    __tablename__ = 'resena'
    id_resena = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match_trabajo.id_match'), nullable=False, unique=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    prestador_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    comentario = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Reseña del cliente {self.cliente_id} para el prestador {self.prestador_id}>'


class Calificacion(db.Model, TimeStampMixin):
    __tablename__ = 'calificacion'
    id_calificacion = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match_trabajo.id_match'), nullable=False)
    autor_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    receptor_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    puntuacion = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        CheckConstraint('puntuacion >= 1 AND puntuacion <= 5', name='Verifica_puntuación'),
        db.UniqueConstraint('match_id', 'autor_id', name='calificacion_unica')
    )
    autor = db.relationship('Usuario', foreign_keys=[autor_id], backref='calificaciones_realizadas')
    receptor = db.relationship('Usuario', foreign_keys=[receptor_id], backref='calificaciones_recibidas')
    match = db.relationship('MatchTrabajo', backref='calificaciones')

    def __repr__(self):
        return f'<Calificación de {self.autor_id} a {self.receptor_id} con {self.puntuacion} estrellas>'


class ImagenGaleria(db.Model, TimeStampMixin):
    __tablename__ = 'galeria_usuario'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    imagen_url = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.String(255), default='')

    usuario = db.relationship('Usuario', backref='galeria')