from configuracion import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Permiso(Base):
    __tablename__ = "permisos"

    id = Column(Integer, primary_key=True, index=True)
    id_rol = Column(Integer, ForeignKey("roles.id"))
    id_reporte = Column(Integer, ForeignKey("reportes.id"))
    id_tipo_permiso = Column(Integer)  # 1=Ver, 2=Exportar, etc.

    rol = relationship("Rol", back_populates="permisos")
    reporte = relationship("Reporte", back_populates="permisos")
