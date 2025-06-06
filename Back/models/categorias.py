from extensions import db

usuario_servicio = db.Table('usuario_servicio',
                            db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id_usuario'), primary_key=True),
                            db.Column('servicio_id', db.Integer, db.ForeignKey('servicio.id_servicio'), primary_key=True))


class CategoriaPrincipal(db.Model):
    __tablename__ = 'categoria_principal'
    id_categoria_principal = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    subcategorias = db.relationship('Subcategoria', backref='categoria_principal', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<CategoriaPrincipal {self.nombre}>'


class Subcategoria(db.Model):
    __tablename__ = 'subcategoria'
    id_subcategoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text)
    categoria_principal_id = db.Column(db.Integer, db.ForeignKey('categoria_principal.id_categoria_principal'), nullable=False)
    servicios = db.relationship('Servicio', backref='subcategoria', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<subcategoria {self.nombre}>'


class Servicio(db.Model):
    __tablename__ = 'servicio'
    id_servicio = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text)
    subcategoria_id = db.Column(db.Integer, db.ForeignKey('subcategoria.id_subcategoria'), nullable=False)
    prestadores = db.relationship('usuario', secondary=usuario_servicio, backref='servicio', lazy='dynamic')
    presupuestos = db.relationship('Presupuesto', backref='servicio', lazy=True)

    def __repr__(self):
        return f'<Servicio {self.nombre}>'
