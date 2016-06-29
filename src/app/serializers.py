from flaskutils.serializers import BaseSerializer


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
