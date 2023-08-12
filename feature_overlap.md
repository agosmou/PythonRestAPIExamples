# Connexion vs Flassger Feature Overlap

## Connexion

`Connexion` is a spec-first web framework. Writing the API specification automatically creates the desired functionality. 

It is worth noting that `connexion` does not strictly require each endpoint to be registered in  

`Connexion` feature set includes:

* Automatic url routing to py functions
* Authentication
* Request Validation
* Parameter parsing and injection
* Response serialization
* Response validation
* Swagger UI

### Tools to help write API specifications

* [Online Swagger UI editor1](https://editor.swagger.io/)
* [VS Code OpenAPI (Swagger) Editor](https://marketplace.visualstudio.com/items?itemName=42Crunch.vscode-openapi)
  * Requires free account to use
* [REST API Design Guidelines](https://opensource.zalando.com/restful-api-guidelines/#table-of-contents)

### How does connexion add OpenAPI features?

`connexion` works as an Asynchronous Server Gateway Interface (ASGI) middleware stack wrapper around python applications.

Since `connexion` works as a "middleware" stack, its functionality can be opaque to the python application writers. The middleware functionality, however, is nicely encapsulated in a collection of middleware classes that operation on requests using a well defined order.

Custom middleware can be registered with `connexion` if necessary. Doing so would require understanding the type of middleware that `connexion` applies, and the relative application order of each middleware.

The standard middleware classes include:

* ExceptionMiddleware: Handles exceptions raised by the middleware stack or application
* SwaggerUIMiddleware: Adds a Swagger UI to your application
* RoutingMiddleware: Routes incoming requests to the right operation defined in the specification
* SecurityMiddleware: Checks incoming requests against the security defined in the specification
* RequestValidationMiddleware: Validates the incoming requests against the spec
* ResponseValidationMiddleware: Validates the returned responses against the spec, if activated
* LifespanMiddleware: Allows registration of code to run before application start-up or after shut-down
* ContextMiddleware: Makes several request scoped context variables available to the application

Each of these middleware objects depend directly on the OpenAPI specification. If the endpoint's OpenAPI registration does not contain all of the information required by the middleware, then the middleware will have no effect. For example, if the endpoint specification does not include any request validation, then the `RequestValidationMiddleware` will do nothing.

## Validation Example -- Get

`Connexion` can automatically validation input. The following simple endpoint demonstrates this.

```yaml
  /user:
    get:
      operationId: "users.get"
      parameters:
        - name: username
          description: Return the user with username 
          in: query
          required: true
          schema:
            type: string
      responses:
        "200":
          description: "Successfully found user"
        "450":
          description: "User not found"
```

```python
def get(username):
    '''
    Database currently contains two users - myemail@email.com & youremail@email.com
    '''
    user = User.query.filter(User.username==username).one_or_none()
    return user_schema.dump(user)
```

The following requests return the following responses:

* `/user` -> 400, Missing 'username' query parameter
* `/user/username` -> 404, URL not found
* `/user?username=invalidUser` -> "{}", 200
  * Returns empty json but successful error code
* `/user?username=myemail@email.com`
  * Returns nonempty json given below and successful error code
* `user?username=myemail@email.com&name=Josh`
  * The return value here depends on the API configuration. If strict validation is enabled (e.g `app.add_api("ex.yaml", strict_validation=True)`) then this would return a 400 error of "Extra query parameter(s) name not in spec". If disabled, then the query would succeed.

```json
{
  "fname": "Chamoy",
  "lname": "Douglas",
  "mname": "Ray",
  "password": "superSecretPass",
  "user_id": 1,
  "username": "myemail@email.com"
}
```

## Validation example -- Create

