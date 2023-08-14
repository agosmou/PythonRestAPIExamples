# Open API Tools

## Requirements

* Route requests to endpoint functions
* Validate request json
* [Optional] Validate response json
* Deserialize request json into typed endpoint parameters
* [Optional] Model object Json serialization and deserialization
  * Optional because model objects are independent of API input/output parameter schema
* HTTPS support, to encrypt communications
* Request authentication
* Endpoint role based access
* [Optional] Swagger UI for easy debugging

## Request Routing

### Connexion

Routing paths are specified within the openAPI yaml. The routing rules can be customized while adding the api. If no resolver is specified (`resolver=None`), then connexion will use their default `connexion.resolver.Resolver` class.

`app.add_api('swagger.yaml', resolver=Resolver())`

```yaml
servers:
  - url: "/v1.2" # define the API base url

paths:
  /endpoint1: # http://HOST/v1.2/endpoint1 
    get:
      operationId: pymodule.pyfunction_get
      # ignore content for now
    post:
      operationId: pymododule.pyfunction_post
      # ignore request body and response content
    #etc
  /endpoint2: # http://HOST/v1.2/endpoint1 
    get:
      x-openapi-router-controller: users # define local relative path
      operationId: pyfunction_delete
```

Using `x-openapi-router-controller` is optional. This declaration will make the `operationId` relative. Note: `x-swagger-router-controller` is an outdated version of `x-openapi-router-controller`. Since we use OpenAPI 3.0 there is no reason to ever use this.

Custom resolvers can be used to edit the relative path of all `operationId`s. For example, all of our endpoints currently look like this:

```yaml
## Current HUU yaml pattern
path:
  /HUUEndpoint:
    get:
      operationId: func_name # First-time reader: "Is this an Id or function?"
      ## several lines down
      x-openapi-router-controller: openapi_server.controllers.controller_module
```

If we specify the proper `RelativeResolver` then we can remove each of these `x-openapi-router-controller` calls.

`app.add_api('swagger.yaml', resolver=RelativeResolver('api'))`

```yaml
## Simpler HUU yaml pattern
path:
  /HUUEndpoint:
    get:
      operationId: controller_module.func_name # First-time reader: "I recognize that module!"
```

### Flask

`connexion` does nothing to enforce OpenAPI compliant endpoint routing for endpoints that are omitted from the specification. This means that developers can quickly standup endpoints for testing purposes, before writing any OpenAPI specification code.

```python
from flask import Flask, jsonify
'''
These 'raw' flask endpoints can be used alongside our OpenAPI endpoints.
They will be missing the connexion configured features (schema validation,
authentication, swagger UI, etc). 

Also - the main module method needs to import the module containing
these endpoints. If the dev forgets this registration step, then the
endpoint will be silently left out of the API
'''
@app.route('/data', methods=['POST'])
def receive_data():
  '''
  # call by doing something like this
  curl -X POST -H "Content-Type: application/json" -d '{"key": "value"}' http://127.0.0.1:5000/data
  '''
  data = request.json
  return jsonify(data)

@app.route('/item/<int:item_id>', methods=['GET'])
def get_item(item_id):
  '''curl http://127.0.0.1:5000/item/123'''
  # For this example, let's just return the received ID in a JSON response.
  return jsonify({"received_id": item_id})
```

## Validate request json

HTTP requests can contain a lot different types of information. A robust framework should parse this information and validate that it matches our API specification expectations before invoking our endpoint function.

* Request line -> Validate that the endpoint exists for the method and URL
* Query Parameters -> Validate that all required query parameters are present and the correct type. Convert each parameter to the correct type.
* Request body -> Validate that the body content type is correct

### Connexion

`connexion` can validate query parameters and body content-type, and cast each individual parameter to the correct native python type (`int`, `str`, `float`, `bool`, `list`, `None`, `dict`). If any required parameters are missing, or if any of the type casts fail, then the request will never reach the endpoint.

To enable the validation the parameter types have to be defined. They can be defined as standalone, reusable, schema - or inline with the endpoint declaration.

```yaml

  /user:
    get:
      operationId: "users.get"
      parameters:
        - name: username
          in: query # other values: header, path, cookie, body
          # for example if specifying header then 
          # curl -X 'GET' 'http://127.0.0.1:8000/0.1/user' -H 'accept: application/json' -H 'username: username'
          required: true
          schema:
            type: string # simple, inline schema
      responses:
        "200":
          description: "Successfully found user"
          content:
            application/json:
              schema: # reusable schema
                $ref: '#/components/schemas/getUser'
  /users:
    get:
      operationId: "users.get_all"
      responses:
        "200":
          description: "Successfully read all users"
          content:
            application/json:
              schema: 
                type: array 
                items:
                  $ref: '#/components/schemas/createUser'
components:
  schemas:
    getUser:
      type: object
      properties:
        fname:
          type: string
        mname:
          type: string
        lname:
          type: string
        username:
          type: string

    createUser:
      allOf: # schemas can be generated from other schema!
        - $ref: '#/components/schemas/getUser'
        - type: object
          properties:
            password:
              type: string
```

## [Optional] Validate response json

Behavior is very similar to the request validation. Major difference is that response validation is disabled by default by connexion. Since we have control over response types, response validation is primarily used as a development tool.

`app.add_api('my_api.yaml', validate_responses=True)`

## Deserialize request json into typed endpoint parameters

Schema is used for more than validation.

## [Optional] Model object Json serialization and deserialization

Optional because model objects are independent of API input/output parameter schema

## HTTPS support, to encrypt communications

OpenAPI does allow you to specify a https server URL, but connexion does not use or enforce this information.

HTTPS support is typically enabled using a reverse proxy, such as `nginx`. With this setup `nginx` would be configured with a ssl certificate. `nginx` performs the TLS handshake to establish the session, decrypts requests to send to the application, and encrypts responses sent from the application.

You can enable https support directly (i.e. for development purposes) by passing in a ssl context, but the ssl context is not actually handled by `flask` or `connexion` - it is actually passed directly to the HTTP server [werkzeug](https://connexion.readthedocs.io/en/latest/security.html#id3) by default.

```python
from OpenSSL import SSL
context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file('yourserver.key')
context.use_certificate_file('yourserver.crt')
# neither connexion nor flask provides a 
# ssl_context parameter!
app.run(host='127.0.0.1', port='12344',
        debug=False/True, ssl_context=context)
```

## Request authentication

## Endpoint role based access

## [Optional] Swagger UI for easy debugging

## Connexion

Swagger UI will 'just work' if the optional swagger dependency is specified and we add a yaml open api specification. `connexion` creates the swagger UI doc using the OpenAPI yaml file.

`pip install connexion[swagger-ui]`

By default the ui will located at `baseURL/ui`. You can, however, specify a custom path if desired:

```python
options = {'swagger_url': '/'}
app = connexion.App(__name__, options=options)
```

The OpenAPI spec has some optional fields that can be used to provide more detailed OpenAPI documentation.

![example-swagger](example_swagger.png)

## Flask

`swagger` is a standalone tool, and we can use it without `connexion` if we properly define our API. This typically requires writing the api specification, but there are some tools to help.

### Flassger

Flasgger allows you to specify swagger UI through the endpoint docstring. It also supports storing as a `yaml` file.

```python
from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """
    Get Item by ID
    ---
    tags:
      - Items
    parameters:
      - name: item_id
        in: path
        type: integer
        required: true
        description: ID of the item
    responses:
      200:
        description: Item retrieved
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
    """
    return jsonify({"id": item_id, "name": "Example Item"})
```

## Overview

Options:

1. spec-first with connexion.
   * Response and request schema declared directly in yaml 

Compare connexion with another popular python API tool. Need to understand their feature set overlap. We should also create some demos to show how to setup simple APIs using both frameworks.

## Questions

### What is OpenAPI?

### Marshmellow + SQLAlchemy

Here’s an example using Flask SQLAlchemy and Marshmallow
https://marshmallow.readthedocs.io/en/stable/examples.html#quotes-api-flask-sqlalchemy

### Flasgger

https://github.com/flasgger/flasgger

### Connexion

https://connexion.readthedocs.io/en/latest/

## Conclusion
