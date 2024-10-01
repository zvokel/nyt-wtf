from typing import Optional

from pydantic import BaseModel
import datetime
from .models import SpellingBee, Sudoku


class SpellingBeeCache(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    last_check: datetime.datetime
    date: datetime.date
    sb: SpellingBee
    first: bool


class SudokuCache(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    last_check: datetime.datetime
    date: datetime.date
    sudoku: Sudoku
    first: bool
