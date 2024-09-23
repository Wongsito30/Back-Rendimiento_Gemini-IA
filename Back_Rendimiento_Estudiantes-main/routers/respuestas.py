from fastapi import APIRouter, Request ,HTTPException, status
from fastapi.responses import JSONResponse
from typing import List
from starlette.responses import RedirectResponse
from sqlalchemy.orm import session
from fastapi.params import Depends

from BD.Connn import engine, sessionlocal
import BD.schemas as page_schemas
import BD.Connn as page_conexion
import BD.modelos as page_models
from geminiAPI import prompt_gen


page_models.Base.metadata.create_all(bind=engine)
router = APIRouter()


def get_respuestas():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()

@router.get("/respuestas")
async def Main():
    return RedirectResponse(url="/docs/")

@router.get("/VerRespuestasPorNickname/{Nickname}")
async def VER_Res_nickname(Nickname: str,db:session=Depends(get_respuestas)):
    ponderaciones = db.query(page_models.Respuestas).filter_by(nickname=Nickname).first()
    return ponderaciones

@router.get("/gemini/{Respuesta_id}/{Nickname}")
async def gemini_AI(idcuestionario: int, Nickname: str,db:session=Depends(get_respuestas)):
    # Seleccionar solo las columnas de preguntas y ponderación
    preguntas = db.query(page_models.Preguntas.pregunta).filter_by(id_cuestionario=idcuestionario).all()
    ponderaciones = db.query(page_models.Respuestas.ponderacion).filter_by(id_cuestionario=idcuestionario, nickname=Nickname).all()
    if not preguntas and not ponderaciones: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no se pudo encontrar preguntas y/o respuestas")
    # Devolver las columnas en un formato adecuado
    data = {"preguntas": [pregunta[0] for pregunta in preguntas], "ponderaciones": [ponderacion[0] for ponderacion in ponderaciones]}

    prompt = "De estas preguntas y respuestas ayudame a predecir el rendimiento academico, las respuestas son del 1-5"
    respuesta = prompt_gen(prompt, data)
    res = page_models.Resultados(nickname=Nickname, id_cuestionario=idcuestionario, resultados=respuesta)
    if not res: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no se pudo guardar el resultado")
    db.add(res)
    db.commit()
    db.refresh(res)
    return respuesta

@router.get("/verRespuestas/", response_model=List[page_schemas.respuestas])
async def show_Respuestas(db:session=Depends(get_respuestas)):
    respuesta = db.query(page_models.Respuestas).all()
    return respuesta

@router.post("/registrarRespuestas/",response_model=page_schemas.respuestas)
def create_respuestas(entrada:page_schemas.respuestas,db:session=Depends(get_respuestas)):
   respuestas = page_models.Respuestas(id_cuestionario = entrada.id_cuestionario, id_pregunta = entrada.id_pregunta, 
                                       nickname = entrada.nickname, ponderacion = entrada.ponderacion)
   db.add(respuestas)
   db.commit()
   db.refresh(respuestas)
   return respuestas

@router.put("/CambiarRespuestas/{Respuesta_id}",response_model=page_schemas.respuestas)
def mod_respuestas(respuestasid: int, entrada:page_schemas.respuestas,db:session=Depends(get_respuestas)):
    respuestas = db.query(page_models.Respuestas).filter_by(id=respuestasid).first()
    respuestas.id_cuestionario = entrada.id_cuestionario 
    respuestas.id_pregunta = entrada.id_pregunta
    respuestas.nickname = entrada.nickname
    respuestas.ponderacion = entrada.ponderacion
    db.commit()
    db.refresh(respuestas)
    return respuestas

@router.put("/CambiarRespuesta/{Id_respuesta}",response_model=page_schemas.cambiarRespuestas)
def mod_RespuestasUsuario(idrespuesta: int, entrada:page_schemas.cambiarRespuestas,db:session=Depends(get_respuestas)):
    respuestas = db.query(page_models.Respuestas).filter_by(id=idrespuesta).first()
    respuestas.ponderacion = entrada.ponderacion
    db.commit()
    db.refresh(respuestas)
    return respuestas

@router.delete("/EliminarRespuestas/{respuestas_id}",response_model=page_schemas.respuesta)
def del_respuestas(respuestasid: int,db:session=Depends(get_respuestas)):
    respuestas = db.query(page_models.Respuestas).filter_by(id=respuestasid).first()
    db.delete(respuestas)
    db.commit()
    respuesta = page_schemas.respuesta(mensaje="Eliminado exitosamente")
    return respuesta