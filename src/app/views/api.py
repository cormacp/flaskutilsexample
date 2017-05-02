from flask import request
from flaskutils import app
from flaskutils.views import BaseResourceView
from pgsqlutils.orm import Session
from sqlalchemy.exc import DataError, IntegrityError
from pgsqlutils.orm import NotFoundError
from app.models import Genre
from app.serializers import PostGenreSerializer
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


class GenreResourceView(BaseResourceView):
    """
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
