# Flask utils example project

[![CircleCI](https://circleci.com/gh/Riffstation/flaskutilsexample.svg?style=svg)](https://circleci.com/gh/Riffstation/flaskutilsexample)

## Introduction
The FlaskUtilsExample application is a simple introduction to a Flask application, built with our FlaskUtils library. The project contains:
* An example **Artist** resource endpoint
* Full CRUD (Create, Remove, Update, Delete) support for the **Artist** endpoint
* Example usage of FlaskUtils' **app**, **view**, **model**, **exception**, **serializers** and **test** modules
* Sample Unit tests for each supported CRUD method
* Factory function for populating the DB with a minimum set of sample data

## Resources


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
