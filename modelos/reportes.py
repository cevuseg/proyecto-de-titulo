from configuracion import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Reporte(Base):
    __tablename__ = "reportes"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    descripcion = Column(String(500))
    url_powerbi = Column(String(500), nullable=False)
    area = Column(String(100))
    id_usuario_subio = Column(Integer, ForeignKey("usuarios.id"))

    usuario_subio = relationship("Usuario", back_populates="reportes")
    permisos = relationship("Permiso", back_populates="reporte")
    accesos = relationship("LogAcceso", back_populates="reporte")
