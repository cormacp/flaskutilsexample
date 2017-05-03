from flask import request
from flaskutils import app
from flaskutils.views import BaseResourceView
from flaskutils.exceptions import SerializerError
from pgsqlutils.orm import Session
from sqlalchemy.exc import DataError, IntegrityError
from pgsqlutils.orm import NotFoundError
from app.models import Genre, Artist
from app.serializers import PostGenreSerializer, GetArtistSerializer, PutArtistSerializer
from jsonschema import ValidationError
from werkzeug.exceptions import BadRequest


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
    Sample endpoint that supports GET and PUT requests
    Includes likely error handling for a GET/PUT endpoint
    """

    methods = ['GET', 'PUT']


    def get(self, **kwargs):
        try:
            if 'uuid' in kwargs:
                artist = Artist.objects.get(key=kwargs['uuid'])
                data = GetArtistSerializer(model=artist).to_json()
                # return self.json_response(
                #     200, {'artist': artist})
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


class GenreResourceView(BaseResourceView):
    """
    Sample endpoint that supports POST requests
    Includes likely error handling for a POST endpoint
    """
    methods = ['POST']

    def post(self):
        try:
            serialized_data = PostGenreSerializer(data=request.json).to_json()
            genre_obj = Genre(**serialized_data)
            genre_obj.add()
            self.PGSession.commit()

            app.logger.info(
                'genre with id {} has been created'.format(genre_obj.id))
            return self.json_response(status=201, data={'id': genre_obj.id})

        except BadRequest:
            return self.json_response(status=400)

        except DataError as e:
            app.logger.info('data error : {}'.format(e))
            self.PGSession.rollback()
            return self.json_response(status=400)

        except AssertionError:
            return self.json_response(status=400)

        except IntegrityError as e:
            app.logger.info('integrity error : {}'.format(e))
            self.PGSession.rollback()
            return self.json_response(status=400)

        except ValidationError as e:
            app.logger.info('request validation error : {}'.format(e))
            self.PGSession.rollback()
            return self.json_response(status=400)

        except Exception as e:
            app.logger.error(e)
            self.PGSession.rollback()
            return self.json_response(status=500)
