from flaskutils import app
from flaskutils.views import BaseView



class ApiDescription(BaseView):
    """
    This initial well known URI (the root URI) provides an endpoint that
    describes the API resources available by request
    """
    methods = ['GET']

    def get(self):
        # Obtain our root hostname from app config
        baseHostname = app.config['BASE_HOSTNAME']

        responseObj = {}
        responseObj['version'] = '2.0'

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
        return self.json_response(200, **data)
