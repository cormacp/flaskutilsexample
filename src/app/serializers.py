from flaskutils.serializers import BaseSerializer
from flaskutils.serializers import uuid_schema


class PostGenreSerializer(BaseSerializer):
    """
    Post requests don't required id as they mean to be
    used for create new objects
    """
    _schema = {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'description': {'type': 'string'},
        },
        'required': ['name']
    }


class GetArtistSerializer(BaseSerializer):
    """
    GET responses require :
        id, name
    """
    _schema = {
        'type': 'object',
        'definitions': {
            'key': uuid_schema,
        },
        'properties': {
            'key': {'$ref': '#/definitions/key'},
            'name': {'type': 'string', 'minLength': 1},
            'image': {'type': 'string'},
            'members': {'type': 'array'},
            'related_artists': {'type': 'array'},
            'is_popular': {'type': 'boolean'},
            'first_character': {'type': 'string'},
            'extra_params': {'type': 'object'}
        },
        'required': [
            'id', 'name']
    }
