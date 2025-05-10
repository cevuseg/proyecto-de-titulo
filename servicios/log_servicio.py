from modelos.log_acceso import LogAcceso
from sqlalchemy.orm import Session

def registrar_acceso(db: Session, id_usuario: int, id_reporte: int):
    log = LogAcceso(
        id_usuario=id_usuario,
        id_reporte=id_reporte
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
