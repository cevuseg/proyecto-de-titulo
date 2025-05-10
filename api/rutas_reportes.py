from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from esquemas.reporte_schema import ReporteCrear
from servicios.reporte_servicio import crear_reporte, obtener_reportes, obtener_reporte_por_id
from configuracion import SessionLocal

router = APIRouter(prefix="/reportes", tags=["Reportes"])

def obtener_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("")
def subir_reporte(reporte: ReporteCrear, db: Session = Depends(obtener_db)):
    return crear_reporte(db, reporte)

@router.get("")
def listar_reportes(db: Session = Depends(obtener_db)):
    return obtener_reportes(db)

@router.get("/{id_reporte}")
def ver_reporte(id_reporte: int, db: Session = Depends(obtener_db)):
    return obtener_reporte_por_id(db, id_reporte)
