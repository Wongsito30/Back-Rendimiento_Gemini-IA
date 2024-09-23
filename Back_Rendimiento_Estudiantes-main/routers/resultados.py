from fastapi import APIRouter,HTTPException
from typing import List
from starlette.responses import RedirectResponse
from sqlalchemy.orm import session
from fastapi.params import Depends
from BD.Connn import engine, sessionlocal
import BD.schemas as page_schemas
import BD.Connn as page_conexion
import BD.modelos as page_models

page_models.Base.metadata.create_all(bind=engine)
router = APIRouter()


def get_resultados():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()

@router.get("/resultados")
async def Main():
    return RedirectResponse(url="/docs/")

@router.get("/verResultados/", response_model=List[page_schemas.Resultados])
async def show_Resultado(db:session=Depends(get_resultados)):
    resultado = db.query(page_models.Resultados).all()
    return resultado

@router.post("/registrarResultado/", response_model=page_schemas.ResultadosCreate)
def create_resultado(entrada: page_schemas.ResultadosCreate, db: session = Depends(get_resultados)):
    # Crea un nuevo resultado en la base de datos
    nuevo_resultado = page_models.Resultados(resultados=entrada.resultados)
    nuevo_resultado.nickname = entrada.nickname
    nuevo_resultado.id_cuestionario = entrada.id_cuestionario
    db.add(nuevo_resultado)
    db.commit()
    db.refresh(nuevo_resultado)

    return nuevo_resultado

@router.put("/CambiarResultado/{resultado_id}",response_model=page_schemas.ResultadosBase)
def mod_resultado(resultado_id: int, entrada:page_schemas.ResultadosBase,db:session=Depends(get_resultados)):
    resultado = db.query(page_models.Resultados).filter_by(id=resultado_id).first()
    resultado.resultados = entrada.resultados
    db.commit()
    db.refresh(resultado)
    return resultado

@router.delete("/EliminarResultado/{resultado_id}",response_model=page_schemas.respuesta)
def del_resultado(resultado_id: int,db:session=Depends(get_resultados)):
    resultado = db.query(page_models.Resultados).filter_by(id=resultado_id).first()
    db.delete(resultado)
    db.commit()
    respuesta = page_schemas.respuesta(mensaje="Eliminado exitosamente")
    return respuesta