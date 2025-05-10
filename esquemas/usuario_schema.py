from pydantic import BaseModel

class UsuarioCrear(BaseModel):
    nombre: str
    correo: str
    contrasena: str
    id_rol: int

class UsuarioRespuesta(BaseModel):
    id: int
    nombre: str
    correo: str
    id_rol: int
    activo: bool

    class Config:
        orm_mode = True
