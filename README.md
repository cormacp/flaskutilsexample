# Flask utils example project

[![CircleCI](https://circleci.com/gh/Riffstation/flaskutilsexample.svg?style=svg)](https://circleci.com/gh/Riffstation/flaskutilsexample)

## Introduction
The FlaskUtilsExample application is a simple introduction to a Flask application, built with our FlaskUtils library. The project contains:
* An example **Artist** resource endpoint
* Full CRUD (Create, Remove, Update, Delete) support for the **Artist** endpoint
* Example usage of FlaskUtils' **app**, **view**, **model**, **exception**, **serializers** and **test** modules
* Sample Unit tests for each supported CRUD method
* Factory function and console command for populating the DB with a minimum set of sample data

## Resources

Our application uses an example **Artist** model as the basis for a full CRUD implementation. The following table shows the structure of a sample **Artist** object:

### Artist

|  Field name          | Type             | Description               | Validations           | Read Only |
| -------------------- | -----------------| ------------------------- | --------------------- | --------- |
|  key                 | UUID             | Account identifier        | * Unique              | YES       |
|                      |                  |                           | * Required            |           |
|  name                | character        |                           | * Required            | NO        |
|                      |                  |                           | * Unique for artis    |           |
|  image               | character        | image url                 |                       | NO        |
|  members             | ARRAY[uuid]      | array of artist members   |                       | NO        |
|  relater_artists     | ARRAY[uuid]      | array of related artists  |                       | NO        |
|  is_popular          | boolean          | popular artist flag       |                       | NO        |
|  first_character     | character        | first character of name   |                       | NO        |
|  extra_params        | JSON object      | object for misc params    |                       | NO        |

## Using the FlaskUtilsExample application

### Running an application instance
To run a listening instance of the application, issue the following commands:
```
    cd ~/src/fender/flaskutilsexample
    vagrant up
    vagrant ssh
    cd /src/src
    python3 manage.py runserver
```
...this will start an instance of our FlaskUtilsExample application, which is accessible at http://192.168.30.133:8080

### Running unit tests
This example application includes a sample suite of unit tests. Each resource method (GET, POST, PUT, DELETE) has two simple unit tests; a valid successful request, and an invalid but correctly handled request. To run this suite of tests:

```
    vagrant ssh
    cd /src/src
    python3 manage.py test

    vagrant@debian-jessie:/src/src$ python3 manage.py test
    ================================================================================ test session starts =================================================================================
    platform linux -- Python 3.4.2, pytest-3.0.7, py-1.4.33, pluggy-0.4.0
    rootdir: /src/src, inifile:
    collected 9 items

    tests/test_views.py ...--------------------------------------------------------------------------------

    ============================================================================== 9 passed in 0.34 seconds ==============================================================================
    vagrant@debian-jessie:/src/src$

```

### Generating sample DB data
To create a set of basic sample data for manual testing:
```
    vagrant ssh
    cd /src/src
    python3 manage.py populate_db

    Generating sample data:
    artists...
    Sample db population complete...

```

## Example Requests
The following requests are syntactically valid FlaskUtilsExample requests for each CRUD method

### GET / Read
```
    curl -X GET \
    http://192.168.30.133:8080/artists/72de1ad1-7234-496f-8faf-520571c48648
```
...sample response:
```
    {
      "artist": {
        "extra_params": null,
        "first_character": "d",
        "id": "72de1ad1-7234-496f-8faf-520571c48648",
        "image": "http://www.imageurl.com/image.jpeg",
        "is_popular": true,
        "members": [],
        "name": "d9c5yi",
        "related_artists": []
      }
    }
```

### POST / Create
```
    curl -X POST \
      http://192.168.30.133:8080/artists \
      -H 'cache-control: no-cache' \
      -H 'content-type: application/json' \
      -d '{
      "name": "New Artist",
      "image": "http://imageurl.jpeg",
      "members": [
        "11c03524-1911-433f-bf86-f234cacd5bcf",
        "a503faf9-45b5-4fec-8334-337284a66ea4"
      ],
      "related_artists": [
        "079117d5-8fcc-4f11-82d8-0f975a408b12",
        "3d49a1f9-3b1f-491c-b504-a5f4190b802c"
      ],
      "is_popular": true
    }'
```
...sample response:
```
    {
      "id": "fc75a21e-dbf7-4c77-b27b-38784d45d2b5"
    }
```

### PUT / Update
```
    curl -X PUT \
      http://192.168.30.133:8080/artists/fc75a21e-dbf7-4c77-b27b-38784d45d2b5 \
      -H 'cache-control: no-cache' \
      -H 'content-type: application/json' \
      -d '{
      "id": "fc75a21e-dbf7-4c77-b27b-38784d45d2b5",
      "name": "Ammended Artist Name",
      "image": "http://imageurl.jpeg",
      "members": [
        "11c03524-1911-433f-bf86-f234cacd5bcf",
        "a503faf9-45b5-4fec-8334-337284a66ea4"
      ],
      "related_artists": [
        "079117d5-8fcc-4f11-82d8-0f975a408b12",
        "3d49a1f9-3b1f-491c-b504-a5f4190b802c"
      ],
      "is_popular": true
    }'
```
...sample response:
```
    {
      "artist": {
        "id": "fc75a21e-dbf7-4c77-b27b-38784d45d2b5",
        "image": "http://imageurl.jpeg",
        "is_popular": true,
        "members": [
          "11c03524-1911-433f-bf86-f234cacd5bcf",
          "a503faf9-45b5-4fec-8334-337284a66ea4"
        ],
        "name": "Ammended Artist Name",
        "related_artists": [
          "079117d5-8fcc-4f11-82d8-0f975a408b12",
          "3d49a1f9-3b1f-491c-b504-a5f4190b802c"
        ]
      }
    }
```

### DELETE
```
    curl -X DELETE \
      http://192.168.30.133:8080/artists/fc75a21e-dbf7-4c77-b27b-38784d45d2b5 \
      -H 'cache-control: no-cache' \
      -H 'postman-token: 132f3275-95de-7e70-e284-ca88221fe31f'
```
...sample response:
```
    {}
```
