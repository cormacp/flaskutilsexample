from flask import request
from flaskutils import app
from flaskutils.views import BaseResourceView

from pgsqlutils.base import Session

from app.models import Genre
from app.serializers import PostGenreSerializer
from jsonschema import ValidationError


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
            serializer = PostGenreSerializer(request=request)
            genre = Genre(serializer=serializer)
            genre.add()
            Session.commit()
            genre = Genre.objects.get(genre.id)
            app.logger.info(
                'genre with id {} has been created'.format(genre.id))
            return self.json_response(status=201, data={'id': genre.id})

        except ValidationError as e:
            Session.rollback()
            return self.json_response(status=200, data={'msg': str(e)})

        except Exception as e:
            app.logger.error(e)
            Session.rollback()
            return self.json_response(status=500)
