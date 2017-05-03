from flaskutils.test import TransactionalTestCase
from app.models import Genre, Artist
from app.serializers import PostGenreSerializer
from unittest.mock import Mock
from jsonschema import ValidationError
from tests.factory import Factory
import uuid
import json
import pytest


class TestAppCase(TransactionalTestCase):
    def setup(self):
        super(TestAppCase, self).setup()
        self.json_request_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Basic dXNlcjpwYXNz'
        }
        self.factory = Factory(self.PGSession)
        self.factory.clear_artists()

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

    def test_get_artist(self):
        """
        Makes a valid GET request for artist data
        """
        artist = self.factory.get_artist()

        result = self.client.get(
            '/artists/' + str(artist.key),
            headers=self.json_request_headers)

        assert 200 == result.status_code
        data = json.loads(result.get_data().decode('utf-8'))
        # Test for non-empty response JSON
        assert data != {}

        # Traverse into the 'artist' block of JSON
        data = data['artist']
        # Test required values: key, name
        assert 'key' in data
        assert data['key'] is not None
        assert data['key'] == str(artist.key)
        assert 'name' in data
        assert data['name'] is not None
        assert data['name'] == artist.name
        assert data['name'][0].lower() == data['first_character'].lower()

    def test_get_invalid_artist(self):
        """
        Makes a valid GET request for artist data
        """
        artist = self.factory.get_artist()

        result = self.client.get(
            '/artists/' + str(uuid.uuid4()),
            headers=self.json_request_headers)

        assert 404 == result.status_code

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
        assert 400 == result.status_code
        data = json.loads(result.get_data().decode('utf-8'))
        assert data == {}
