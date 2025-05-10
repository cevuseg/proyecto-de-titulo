from pydantic import BaseModel

class ReporteCrear(BaseModel):
    titulo: str
    descripcion: str
    url_powerbi: str
    area: str

class ReporteRespuesta(BaseModel):
    id: int
    titulo: str
    descripcion: str
    url_powerbi: str
    area: str
    id_usuario_subio: int

    class Config:
        orm_mode = True
