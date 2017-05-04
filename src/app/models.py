from flaskutils.models import FlaskModel
from sqlalchemy import (Column, String, Boolean)
from sqlalchemy.dialects.postgresql import (
    ARRAY, JSON, UUID
)


class Artist(FlaskModel):
    __tablename__ = 'artists'
    key = Column(UUID(as_uuid=True), nullable=False, unique=True)
    name = Column(String(256), nullable=False, unique=True)
    image = Column(String(256))
    members = Column(ARRAY(UUID))
    related_artists = Column(ARRAY(UUID))
    is_popular = Column(Boolean, default=False)
    first_character = Column(String(16))
    extra_params = Column(JSON)
