
from datetime import date
from pydantic import BaseModel, EmailStr
from typing import List, Optional

class GastoBase(BaseModel):
    descripcion: str
    categoria: str  
    monto: float
    fecha: date
    metodoPago: str 
    frecuencia: str  

class GastoCreate(GastoBase):
    pass

class Gasto(GastoBase):
    id: int
    class Config:
        orm_mode = True

class MetaAhorroBase(BaseModel):
    nombre_meta: str
    monto_objetivo: float
    fecha_limite: date
    monto_ahorrado: Optional[float] = 0  
    progreso: Optional[float] = 0  
    estado: Optional[str] = 'En progreso'

class MetaAhorroCreate(MetaAhorroBase):
    pass

class MetaAhorro(MetaAhorroBase):
    id: int

    class Config:
        orm_mode = True

class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr 
    saldoActual: float

class UsuarioCreate(UsuarioBase):
    password: str  

class Usuario(UsuarioBase):
    id: int
    gastos: List['Gasto'] = []  # Definición de relación
    metas: List['MetaAhorro'] = []
    
    class Config:
        orm_mode = True

