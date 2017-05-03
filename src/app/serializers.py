from flaskutils.serializers import BaseSerializer
from flaskutils.serializers import uuid_schema
from app.models import Genre, Artist
from decimal import Decimal


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

    def to_json(self):
        data = {}
        for k, v in self.__dict__.items():
            if not k.startswith('_'):
                data[k] = v
            # Cast Numeric data types to float
            if (type(v) == Decimal):
                data[k] = float(v)

        if 'key' in data:
            # Rename 'key' field to 'id'
            data['id'] = data.pop('key')

        return data


class PutArtistSerializer(BaseSerializer):
    """
    PUT responses require :
        id, name
    """
    __model__ = Artist
    _schema = {
        'type': 'object',
        'definitions': {
            'key': uuid_schema,
        },
        'properties': {
            'id': {'$ref': '#/definitions/key'},
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

    def to_json(self):
        data = {}
        for k, v in self.__dict__.items():
            if not k.startswith('_'):
                data[k] = v
            # Cast Numeric data types to float
            if (type(v) == Decimal):
                data[k] = float(v)

        if 'key' in data:
            # Rename 'key' field to 'id'
            data['id'] = data.pop('key')

        return data

    def update(self):
        """
        Finds record and update it based in serializer values
        """
        obj = self.__model__.objects.get(key=self.key)

        for name, value in self.__dict__.items():
            if name in self._properties:
                setattr(obj, name, value)
        obj.update()
        return obj

    def _initialize_from_dict(self, data):
        """
        Loads serializer from a request object
        """
        self._json = data
        self._validate()
        for name, value in self._json.items():
            if name == 'id':
                name = 'key'

            if name in self._properties:
                # applying proper formatting when required
                if 'format' in self._properties[name]:
                    format = self._properties[name]['format']

                    if 'date-time' == format:
                        value = utils.string_to_datetime(value)
                    elif 'date' == format:
                        value = utils.string_to_date(value)
            setattr(self, name, value)
