from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from defs import DB_PATH

db = f"sqlite:///{DB_PATH}"

Base = declarative_base()
engine = create_engine(db, echo=False, pool_pre_ping=True)
DBSession = sessionmaker(bind=engine)
session = DBSession()