from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel

class LoginRequest(BaseModel):
    id: int
    password: str
    

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False) 
    email = Column(String(100), nullable=False, unique=True)  # Asegúrate de que el email sea único
    hashed_password = Column(String(100), nullable=False)  # Campo para la contraseña hasheada
    saldoActual = Column(Float, nullable=False, default=0.0)  
    gastos = relationship("Gasto", back_populates="usuario")
    metas = relationship("MetaAhorro", back_populates="usuario")

class Gasto(Base):
    __tablename__ = "gastos"
    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(255), nullable=False)
    categoria = Column(String(100), nullable=False) 
    monto = Column(Float, nullable=False)
    fecha = Column(Date, nullable=False) 
    metodoPago = Column(String(100), nullable=False) 
    frecuencia = Column(String(100), nullable=False) 
    id_usuario = Column(Integer, ForeignKey("usuarios.id"))
    usuario = relationship("Usuario", back_populates="gastos")

class MetaAhorro(Base):
    __tablename__ = "metas_ahorro"

    id = Column(Integer, primary_key=True, index=True)
    nombre_meta = Column(String(255))  
    monto_objetivo = Column(Float, nullable=False) 
    fecha_limite = Column(String(230))  
    monto_ahorrado = Column(Float, default=0)  
    progreso = Column(Float, default=0)  
    estado = Column(String(100), default='En progreso')  
    id_usuario = Column(Integer, ForeignKey("usuarios.id"))
    usuario = relationship("Usuario", back_populates="metas")