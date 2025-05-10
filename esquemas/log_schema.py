from pydantic import BaseModel
from datetime import datetime

class LogAccesoRespuesta(BaseModel):
    id: int
    id_usuario: int
    id_reporte: int
    fecha_acceso: datetime

    class Config:
        orm_mode = True
