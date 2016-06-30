from flaskutils.test import TransactionalTestCase

from app.models import Genre
from app.serializers import PostGenreSerializer
from unittest.mock import Mock
from jsonschema import ValidationError

import json
import pytest


class TestAppCase(TransactionalTestCase):
    def test_api_root(self):
        """
        Makes a HTTP GET REQUEST AND API information
        I make a request to / and i get information
        about resources
        """
        result = self.client.get('/')
        assert 200 == result.status_code
        data = json.loads(result.get_data().decode('utf-8'))
        assert 'version' in data
        assert '1.0' == data['version']
        assert 'entityMetadata' in data

    def test_post_genre_serializer(self):
        """
        Test correct format for post serializers
        """
        data = {'name': 'rock', 'description': 'nice'}
        request = Mock()
        request.json = data
        PostGenreSerializer(request=request)
        data = {'description': 'nice'}
        request.json = data
        with pytest.raises(ValidationError) as excinfo:
            PostGenreSerializer(request=request)
        assert "'name' is a required property" in str(excinfo.value)

    def test_create_genre(self):
        """
        Makes a post request and create a new genre
        """
        data = {'name': 'rock', 'description': 'nice'}
        assert 0 == Genre.objects.count()
        result = self.client.post(
            '/genres', data=json.dumps(data),
            headers=self.json_request_headers)
        assert 201 == result.status_code
        assert 1 == Genre.objects.count()
        data = {'description': 'nice'}
        result = self.client.post(
            '/genres', data=json.dumps(data),
            headers=self.json_request_headers)
        assert 200 == result.status_code
        data = json.loads(result.get_data().decode('utf-8'))
        assert 'msg' in data
        assert "'name' is a required property" in data['msg']
