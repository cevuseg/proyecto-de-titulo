from configuracion import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from modelos.rol import Rol
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    contrasena = Column(String(200), nullable=False)
    id_rol = Column(Integer, ForeignKey("roles.id"))
    activo = Column(Boolean, default=True)

    rol = relationship("Rol", back_populates="usuarios")
    reportes = relationship("Reporte", back_populates="usuario_subio")
    accesos = relationship("LogAcceso", back_populates="usuario")
