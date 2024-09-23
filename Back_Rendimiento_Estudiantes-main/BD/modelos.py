from sqlalchemy import Column, Integer, String, LargeBinary, Float, Date, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Usuarios(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(50))
    correo = Column(String(200))
    contrasena =  Column(String(1000))
    resultados = relationship("Resultados", back_populates="usuario")
    codigo = Column(Integer)

class Resultados(Base):
    __tablename__ = 'resultados'

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(50))
    id_usuario = Column(Integer, ForeignKey('usuarios.id'))
    usuario = relationship("Usuarios", back_populates="resultados")
    
    id_cuestionario = Column(Integer, ForeignKey('cuestionarios.id'))
    cuestionario = relationship("Cuestionarios", back_populates="resultados")
    resultados = Column(JSON)

class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(50))
    contrasena =  Column(String(1000))
    pruebas = relationship("Pruebas", back_populates="admin_obj")
    resultados = Column(JSON)

class Cuestionarios(Base):
    __tablename__ = 'cuestionarios'

    id = Column(Integer, primary_key=True, index=True)
    preguntas = relationship("Preguntas", back_populates="cuestionario")
    resultados = relationship("Resultados", back_populates="cuestionario")
    pruebas = relationship("Pruebas", back_populates="cuestionario")
    descripcion = Column(String(500))

class Preguntas(Base):
    __tablename__ = 'preguntas'

    id = Column(Integer, primary_key=True, index=True)
    id_cuestionario = Column(Integer, ForeignKey('cuestionarios.id'))
    cuestionario = relationship("Cuestionarios", back_populates="preguntas")
    pregunta = Column(String(500))
    tipo = Column(String(150))

class Respuestas(Base):
    __tablename__ = 'respuestas'

    id = Column(Integer, primary_key=True, index=True)
    id_cuestionario = Column(Integer)
    id_pregunta = Column(Integer)
    nickname = Column(String(50))
    ponderacion = Column(Integer)

class Respuestasprueba(Base):
    __tablename__ = 'respuestasprueba'

    id = Column(Integer, primary_key=True, index=True)
    id_cuestionario = Column(Integer)
    id_pregunta = Column(Integer)
    nickname = Column(String(50))
    ponderacion = Column(Integer)
    
class Pruebas(Base):
    __tablename__ = 'pruebas'

    id = Column(Integer, primary_key=True, index=True)
    admin = Column(String(50))  # Cambié el nombre de la columna admin a admin_name
    id_admin = Column(Integer, ForeignKey('admins.id'))
    
    # Renombramos la relación a admin_obj para evitar conflicto con la columna
    admin_obj = relationship("Admin", back_populates="pruebas") 
    
    id_cuestionario = Column(Integer, ForeignKey('cuestionarios.id'))
    cuestionario = relationship("Cuestionarios", back_populates="pruebas")
    resultados = Column(JSON)