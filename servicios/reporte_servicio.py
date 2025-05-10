from modelos.reportes import Reporte
from esquemas.reporte_schema import ReporteCrear
from sqlalchemy.orm import Session

def crear_reporte(db: Session, reporte: ReporteCrear):
    nuevo_reporte = Reporte(
        titulo=reporte.titulo,
        descripcion=reporte.descripcion,
        url_powerbi=reporte.url_powerbi,
        area=reporte.area
    )
    db.add(nuevo_reporte)
    db.commit()
    db.refresh(nuevo_reporte)
    return nuevo_reporte

def obtener_reportes(db: Session):
    return db.query(Reporte).all()

def obtener_reporte_por_id(db: Session, id_reporte: int):
    return db.query(Reporte).filter(Reporte.id == id_reporte).first()
