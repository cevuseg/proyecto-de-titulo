from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from servicios.usuario_servicio import autenticar_usuario
from configuracion import SessionLocal
from jose import jwt
import os
from datetime import datetime, timedelta
from pydantic import BaseModel
from servicios.usuario_servicio import autenticar_usuario

router = APIRouter(prefix="/login", tags=["Autenticación"])

# Cargar variables de entorno
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

class LoginSchema(BaseModel):
    correo: str
    contrasena: str

def obtener_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("")
def login(datos: LoginSchema, db: Session = Depends(obtener_db)):
    usuario = autenticar_usuario(db, datos.correo, datos.contrasena)
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.encode(
        {"sub": usuario.correo, "exp": datetime.utcnow() + access_token_expires, "rol": usuario.rol.nombre},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {"access_token": access_token, "token_type": "bearer", "rol": usuario.rol.nombre}
