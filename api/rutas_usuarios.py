from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from configuracion import SessionLocal
from modelos.usuario import Usuario

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/correo/{correo}")
def obtener_usuario_por_correo(correo: str, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.correo == correo).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"rol": usuario.rol.nombre}
