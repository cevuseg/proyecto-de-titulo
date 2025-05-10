from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from esquemas.usuario_schema import UsuarioCrear
from servicios.usuario_servicio import crear_usuario, obtener_usuarios
from configuracion import SessionLocal

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

def obtener_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("")
def registrar_usuario(usuario: UsuarioCrear, db: Session = Depends(obtener_db)):
    return crear_usuario(db, usuario)

@router.get("")
def listar_usuarios(db: Session = Depends(obtener_db)):
    return obtener_usuarios(db)
