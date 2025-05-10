from pydantic import BaseModel

class PermisoCrear(BaseModel):
    id_rol: int
    id_reporte: int
    id_tipo_permiso: int

class PermisoRespuesta(BaseModel):
    id: int
    id_rol: int
    id_reporte: int
    id_tipo_permiso: int

    class Config:
        orm_mode = True
