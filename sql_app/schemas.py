from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class MorbidBase(BaseModel):
    classe_age : int
    jour : date
    premiere_dose : int
    deuxieme_dose : int
    premiere_dose_cum : int
    deuxieme_dose_cum: int


class MorbidCreate(MorbidBase):
    pass


class Morbid(MorbidBase):
    classe_age: int
    jour: date
    premiere_dose: int
    deuxieme_dose: int
    premiere_dose_cum: int
    deuxieme_dose_cum: int

    class Config:
        orm_mode = True
