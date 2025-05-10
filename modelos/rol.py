from configuracion import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from modelos.permiso import Permiso


class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)

    usuarios = relationship("Usuario", back_populates="rol")
    permisos = relationship("Permiso", back_populates="rol")
