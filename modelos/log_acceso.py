from configuracion import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class LogAcceso(Base):
    __tablename__ = "logs_acceso"

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"))
    id_reporte = Column(Integer, ForeignKey("reportes.id"))
    fecha_acceso = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="accesos")
    reporte = relationship("Reporte", back_populates="accesos")
