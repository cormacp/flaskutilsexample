from flask import request
from flaskutils import app
from flaskutils.views import BaseResourceView
from flaskutils.exceptions import SerializerError
from pgsqlutils.orm import Session
from sqlalchemy.exc import DataError, IntegrityError
from pgsqlutils.orm import NotFoundError
from app.models import Artist
from app.serializers import GetArtistSerializer, PutArtistSerializer, PostArtistSerializer
from jsonschema import ValidationError
from werkzeug.exceptions import BadRequest
import uuid


class ApiDescription(BaseResourceView):
    """
    This initial well known URI (the root URI) provides an endpoint that
    describes the API resources available by request
    """
    methods = ['GET']

    def get(self):
        # Obtain our root hostname from app config
        baseHostname = app.config['BASE_HOSTNAME']

        responseObj = {}
        responseObj['version'] = '1.0'

        entityMetadata = {}
        entityMetadata['rel'] = 'help'
        entityMetadata['href'] = \
            baseHostname + '/api/entities/'
        responseObj['entityMetadata'] = entityMetadata

        apiDescription = {}
        apiDescription['rel'] = 'API Endpoint description'
        apiDescription['href'] = \
            baseHostname + '/api/'
        responseObj['API Description'] = apiDescription

        data = responseObj
        return self.json_response(200, data=data)


class ArtistResourceView(BaseResourceView):
    """
    Sample endpoint that supports GET, POST, DELETE and PUT requests
    Includes likely error handling for a GET/PUT/POST/DELETE endpoint
    """

    methods = ['GET', 'PUT', 'DELETE', 'POST']


    def get(self, **kwargs):
        try:
            if 'uuid' in kwargs:
                artist = Artist.objects.get(key=kwargs['uuid'])
                data = GetArtistSerializer(model=artist).to_json()

                return self.json_response(
                    200, {'artist': data})
            else:
                return self.json_response(200, {'artist': 'not specified'})

        except NotFoundError as e:
            # REQUEST structure was valid, but ID was invalid. Return 404
            return self.json_response(status=404)

        except ValidationError as e:
            return self.json_response(status=400)

        # General exception handler
        except Exception as e:
            app.logger.info(e)
            return self.json_response(status=500)

    def put(self, **kwargs):
        try:
            if 'uuid' not in kwargs:
                raise ValidationError("Artist not specified")

            target_uuid = kwargs['uuid']
            serializer = PutArtistSerializer(data=request.json)
            assert str(target_uuid) == serializer.key
            obj = serializer.update()
            self.PGSession.commit()

            app.logger.info(
                'artist with id {} has been updated'.format(target_uuid))
            return self.json_response(status=200, data={'artist': serializer.to_json()})

        except DataError as e:
            app.logger.info('data error : {}'.format(e))
            self.PGSession.rollback()
            return self.json_response(status=400)

        except IntegrityError as e:
            app.logger.info('integrity error : {}'.format(e))
            self.PGSession.rollback()
            return self.json_response(status=400)

        except ValidationError as e:
            app.logger.info('validation error : {}'.format(e))
            return self.json_response(status=400)

        except ValueError as e:
            app.logger.info('value error : {}'.format(e))
            return self.json_response(status=400)

        except NotFoundError as e:
            app.logger.info('not found error : {}'.format(e))
            return self.json_response(status=404)

        except AssertionError:
            app.logger.info('assertion error')
            return self.json_response(status=400)

        except BadRequest:
            app.logger.info('bad request')
            return self.json_response(status=400)

        except SerializerError as e:
            app.logger.info('serializer error : {}'.format(e))
            return self.json_response(status=400)

        except Exception as e:
            app.logger.info('general exception : {}'.format(e))
            self.PGSession.rollback()
            return self.json_response(status=500)

    def delete(self, **kwargs):
        try:
            if 'uuid' in kwargs:
                target_uuid = kwargs['uuid']
                target_artist = Artist.objects.get(
                    key=target_uuid)
                if target_artist:
                    target_artist.delete()
                    self.PGSession.commit()
                    return self.json_response(status=200, data={})
            else:
                raise ValidationError("Artist not specified")

        except DataError as e:
            app.logger.info('data error : {}'.format(e))
            self.PGSession.rollback()
            return self.json_response(status=400)

        except NotFoundError as e:
            app.logger.info('not found error : {}'.format(e))
            # REQUEST structure was valid, but ID was invalid. Return 404
            return self.json_response(status=404)

        except ValidationError as e:
            app.logger.info('validation error : {}'.format(e))
            return self.json_response(status=400)

        # General exception handler
        except Exception as e:
            app.logger.info('general exception : {}'.format(e))
            self.PGSession.rollback()
            return self.json_response(status=500)

    def post(self, **kwargs):
        try:
            serialized_data = PostArtistSerializer(data=request.json).to_json()
            serialized_data['key'] = uuid.uuid4()
            obj = Artist(**serialized_data)
            obj.add()
            self.PGSession.commit()
            return self.json_response(
                status=201, data={'id': obj.key}
            )

        except BadRequest:
            app.logger.info('BadRequest error : {}'.format(e))
            return self.json_response(status=400)

        except DataError as e:
            app.logger.info('DataError error : {}'.format(e))
            self.PGSession.rollback()
            return self.json_response(status=400)

        except AssertionError:
            return self.json_response(status=400)

        except IntegrityError as e:
            app.logger.info('IntegrityError error : {}'.format(e))
            self.PGSession.rollback()
            return self.json_response(status=400)

        except ValidationError as e:
            app.logger.info('ValidationError error : {}'.format(e))
            return self.json_response(status=400)

        except ValueError as e:
            app.logger.info('ValueError error : {}'.format(e))
            return self.json_response(status=400)

        except SerializerError as e:
            app.logger.info('SerializerError : {}'.format(e))
            return self.json_response(status=400)

        except Exception as e:
            app.logger.info('General Exception : {}'.format(e))
            app.logger.error(e)
            self.PGSession.rollback()
            return self.json_response(status=500)
