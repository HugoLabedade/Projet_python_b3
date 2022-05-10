from black import Timestamp
from sqlalchemy import Column, Integer
from sqlalchemy.types import Date
from .database import Base


class Morbid(Base):
    __tablename__ = "Morbid"

    classe_age = Column(Integer, primary_key=True)
    jour = Column(Date)
    premiere_dose = Column(Integer)
    deuxieme_dose = Column(Integer)
    premiere_dose_cum = Column(Integer)
    deuxieme_dose_cum = Column(Integer)
