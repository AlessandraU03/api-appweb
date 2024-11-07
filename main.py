from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import crud, models, schemas
from jose import jwt
from models import LoginRequest
from sqlalchemy import text
from datetime import datetime
from datetime import timedelta
from crud import get_password_hash, create_access_token, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = [
    "http://54.147.126.173",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@app.get("/")
def test():
    return {"message": "¡Hola! FastAPI está corriendo correctamente"}

@app.get("/test_db_connection")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        # Realiza una consulta simple, como contar los registros en una tabla específica
        result = db.execute(text("SELECT COUNT(*) FROM gastos"))  # Cambia aquí
        count = result.scalar()  # Obtener el resultado como un solo valor
        return {"message": "Conexión a la base de datos exitosa", "count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")


@app.post("/usuarios/", response_model=schemas.Usuario)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = models.Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@app.get("/usuarios/", response_model=list[schemas.Usuario])
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(models.Usuario).all()
    return usuarios

@app.get("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def leer_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.put("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def actualizar_usuario(usuario_id: int, usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for key, value in usuario.dict().items():
        setattr(db_usuario, key, value)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(db_usuario)
    db.commit()
    return {"mensaje": "Usuario eliminado"}

# -----------------------------------------
#            CRUD para Gasto
# -----------------------------------------

@app.post("/gastos/", response_model=schemas.Gasto)
def crear_gasto(gasto: schemas.GastoCreate, db: Session = Depends(get_db)):
    db_gasto = models.Gasto(**gasto.dict())
    db.add(db_gasto)
    db.commit()
    db.refresh(db_gasto)
    return db_gasto

@app.get("/gastos/", response_model=list[schemas.Gasto])
def listar_gastos(db: Session = Depends(get_db)):
    gastos = db.query(models.Gasto).all()
    return gastos

@app.get("/gastos/{gasto_id}", response_model=schemas.Gasto)
def leer_gasto(gasto_id: int, db: Session = Depends(get_db)):
    gasto = db.query(models.Gasto).filter(models.Gasto.id == gasto_id).first()
    if gasto is None:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    return gasto

@app.put("/gastos/{gasto_id}", response_model=schemas.Gasto)
def actualizar_gasto(gasto_id: int, gasto: schemas.GastoCreate, db: Session = Depends(get_db)):
    db_gasto = db.query(models.Gasto).filter(models.Gasto.id == gasto_id).first()
    if db_gasto is None:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    for key, value in gasto.dict().items():
        setattr(db_gasto, key, value)
    db.commit()
    db.refresh(db_gasto)
    return db_gasto

@app.delete("/gastos/{gasto_id}")
def eliminar_gasto(gasto_id: int, db: Session = Depends(get_db)):
    db_gasto = db.query(models.Gasto).filter(models.Gasto.id == gasto_id).first()
    if db_gasto is None:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    db.delete(db_gasto)
    db.commit()
    return {"mensaje": "Gasto eliminado"}

# -----------------------------------------
#         CRUD para Meta de Ahorro
# -----------------------------------------

@app.post("/metas/", response_model=schemas.MetaAhorro)
def crear_meta(meta: schemas.MetaAhorroCreate, db: Session = Depends(get_db)):
    db_meta = models.MetaAhorro(**meta.dict())
    db.add(db_meta)
    db.commit()
    db.refresh(db_meta)
    return db_meta

@app.get("/metas/", response_model=list[schemas.MetaAhorro])
def listar_metas(db: Session = Depends(get_db)):
    metas = db.query(models.MetaAhorro).all()
    return metas

@app.get("/metas/{meta_id}", response_model=schemas.MetaAhorro)
def leer_meta(meta_id: int, db: Session = Depends(get_db)):
    meta = db.query(models.MetaAhorro).filter(models.MetaAhorro.id == meta_id).first()
    if meta is None:
        raise HTTPException(status_code=404, detail="Meta de ahorro no encontrada")
    return meta

@app.put("/metas/{meta_id}", response_model=schemas.MetaAhorro)
def actualizar_meta(meta_id: int, meta: schemas.MetaAhorroCreate, db: Session = Depends(get_db)):
    db_meta = db.query(models.MetaAhorro).filter(models.MetaAhorro.id == meta_id).first()
    if db_meta is None:
        raise HTTPException(status_code=404, detail="Meta de ahorro no encontrada")
    for key, value in meta.dict().items():
        setattr(db_meta, key, value)
    db.commit()
    db.refresh(db_meta)
    return db_meta

@app.delete("/metas/{meta_id}")
def eliminar_meta(meta_id: int, db: Session = Depends(get_db)):
    db_meta = db.query(models.MetaAhorro).filter(models.MetaAhorro.id == meta_id).first()
    if db_meta is None:
        raise HTTPException(status_code=404, detail="Meta de ahorro no encontrada")
    db.delete(db_meta)
    db.commit()
    return {"mensaje": "Meta de ahorro eliminada"}

@app.delete("/metas/")
def eliminar_todas_las_metas(db: Session = Depends(get_db)):
    try:
        # Elimina todas las metas de ahorro
        metas_eliminadas = db.query(models.MetaAhorro).delete()
        db.commit()
        
        # Verifica si se eliminaron metas
        if metas_eliminadas == 0:
            raise HTTPException(status_code=404, detail="No hay metas de ahorro para eliminar")
        
        return {"mensaje": f"Se eliminaron {metas_eliminadas} metas de ahorro"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar las metas de ahorro: {e}")
