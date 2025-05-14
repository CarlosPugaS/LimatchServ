from datetime import datetime, timezone
from extensions import db

class TimeStampMixin:
  creado_en = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
  actualizado_en = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

  def formato_fecha(self, campo):
    fecha = getattr(self, campo)
    if fecha:
      return fecha.strftime('%d-%m-%Y %H:%M:%S')
    return None
  
  def creado_formato(self):
    return self.formato_fecha('creado_en')
  
  def actualizado_formato(self):
    return self.formato_fecha('actualizado_en')