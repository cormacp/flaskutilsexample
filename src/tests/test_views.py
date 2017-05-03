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
        # Test required values: id, name
        assert 'id' in data
        assert data['id'] is not None
        assert data['id'] == str(artist.key)
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

    def test_put_artist_valid(self):
        """
        Makes a PUT method request and validates responses
        """
        existing_artist = self.factory.get_artist()
        init_artist_count = Artist.objects.count()

        # construct a valid JSON body for a PUT artist request
        put_request_body = {
            "id": str(existing_artist.key),
            "name": "NewArtistName",
            "first_character": "N",
            "extra_params": {"fieldName": "fieldValue"},
            "image": "imageURL",
            "members": [
                "11c03524-1911-433f-bf86-f234cacd5bcf",
                "a503faf9-45b5-4fec-8334-337284a66ea4"
            ],
            "related_artists": [
                "079117d5-8fcc-4f11-82d8-0f975a408b12",
                "3d49a1f9-3b1f-491c-b504-a5f4190b802c"
            ],
            "is_popular": True
        }
        request_url = '/artists/' + str(existing_artist.key)

        result = self.client.put(
            request_url, data=json.dumps(put_request_body),
            headers=self.json_request_headers)

        # Test for valid response code
        assert 200 == result.status_code
        response_data = json.loads(result.get_data().decode('utf-8'))
        # Test for non-empty response JSON
        assert 'artist' in response_data
        # Traverse into the 'artist' block of JSON
        artist_data = response_data['artist']
        # Test required values: id, name
        assert 'id' in artist_data
        assert 'name' in artist_data
        assert Artist.objects.count() == init_artist_count

        # Verify that updated record reflects new values
        get_url = '/artists/' + str(existing_artist.key)
        result = self.client.get(get_url, headers=self.json_request_headers)
        get_response_data = json.loads(result.get_data().decode('utf-8'))
        assert 'artist' in get_response_data
        updated_obj = Artist.objects.get(
            key=get_response_data['artist']['id'])
        assert updated_obj.id == existing_artist.id
        assert updated_obj.name == 'NewArtistName'

    def test_put_artist_unknown_uuid(self):
        """
        Makes a PUT method request and validates responses
        """
        self.factory.get_artist()
        init_artist_count = Artist.objects.count()
        new_uuid = uuid.uuid4()

        # construct a valid JSON body for a PUT artist request
        put_request_body = {
            "id": str(new_uuid),
            "name": "NewArtistName",
            "image": "imageURL",
            "members": [
                "11c03524-1911-433f-bf86-f234cacd5bcf",
                "a503faf9-45b5-4fec-8334-337284a66ea4"
            ],
            "related_artists": [
                "079117d5-8fcc-4f11-82d8-0f975a408b12",
                "3d49a1f9-3b1f-491c-b504-a5f4190b802c"
            ],
            "is_popular": True
        }
        request_url = '/artists/' + str(new_uuid)

        result = self.client.put(
            request_url, data=json.dumps(put_request_body),
            headers=self.json_request_headers)

        # Test for valid response code
        assert 404 == result.status_code
        assert Artist.objects.count() == init_artist_count

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
