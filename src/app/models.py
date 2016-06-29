from flaskutils.models import FlaskModel
from sqlalchemy import Column, String


class Genre(FlaskModel):
    __tablename__ = 'genre'
    name = Column(String(256))
    description = Column(String(256))
