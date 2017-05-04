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

### PUT / Update

### DELETE
