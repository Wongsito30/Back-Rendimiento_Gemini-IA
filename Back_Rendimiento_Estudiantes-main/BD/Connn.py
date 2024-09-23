from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

databaseURL = "mysql+mysqlconnector://root:12345@localhost:5432/RendimientoEstudiantes"

engine = create_engine(databaseURL)

sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base = declarative_base