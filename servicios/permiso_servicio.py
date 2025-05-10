from modelos.permiso import Permiso
from esquemas.permiso_schema import PermisoCrear
from sqlalchemy.orm import Session

def asignar_permiso(db: Session, permiso: PermisoCrear):
    nuevo_permiso = Permiso(
        id_rol=permiso.id_rol,
        id_reporte=permiso.id_reporte,
        id_tipo_permiso=permiso.id_tipo_permiso
    )
    db.add(nuevo_permiso)
    db.commit()
    db.refresh(nuevo_permiso)
    return nuevo_permiso
