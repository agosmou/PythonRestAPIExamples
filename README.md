# How to Build

```shell
cd connexion_api
# create and activate virtual environment
pip install -r requirements.txt
python -m app
```

This should start the demo api using a development server on `http://127.0.0.1:8000`. Check the logs to verify the port number. The api can be accessed most easily from the browser:

See `http://127.0.0.1:8000/0.1/ui` for the Swagger UI.

# Notes
[Original Architecture Analysis and Discovery by Joshua Douglas[(https://github.com/Joshua-Douglas/PythonRestAPIExamples/blob/main/OpenAPI_API_Tools.md)
[Home Unite Us](https://github.com/hackforla/HomeUniteUs)
Architectural Decision Record [ADR](https://github.com/joelparkerhenderson/architecture-decision-record/tree/main/locales/en/templates/decision-record-template-by-michael-nygard)
[Connexion Library](https://github.com/spec-first/connexion)
 



# Connexion vs Traditional Flask API Development

This guide compares how certain tasks are handled with and without the `connexion` library in Python. 

## 1. API-First Design

### With `connexion`:
- Define your API in a YAML or JSON file using the OpenAPI Specification.
- The `connexion` app reads this file and sets up the API.

```yaml
# openapi.yaml
paths:
  /users/{userId}:
    get:
      summary: Get a user by ID
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
```

### Without `connexion`:
- Define routes and handlers directly in Python code, typically using Flask.
- The API's structure is embedded in the code.

```python
# app.py (using Flask)
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/users/<int:userId>', methods=['GET'])
def get_user(userId):
    # Implementation to fetch and return user
    return jsonify({"id": userId, "name": "John Doe"})
```

## 2. Automatic Endpoint Routing

### With `connexion`:
- Routes are automatically set up based on the OpenAPI specification file.
- Each path in the specification is linked to a Python function.

```python
import connexion

app = connexion.App(__name__)
app.add_api('openapi.yaml')

def get_user(userId):
    return {"id": userId, "name": "John Doe"}
```

### Without `connexion`:
- Each route is manually defined in the code.

```python
# app.py (using Flask)
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/users/<int:userId>', methods=['GET']) # manually defined URI
def get_user(userId):
    # Implementation to fetch and return user
    return jsonify({"id": userId, "name": "John Doe"})
```


### 3. Input Validation

#### With `connexion`:
- Input validation is automatically handled based on the OpenAPI spec.
- If a request does not meet the specified parameters, `connexion` returns an error.

#### Without `connexion`, Option 1: Manual Code Validation:
- Manually validate inputs in your function.
- This approach involves explicitly checking the types and values of the inputs.

```python
@app.route('/users/<int:userId>', methods=['GET'])
def get_user(userId):
    if type(userId) is not int:
        return "Invalid input", 400
    # Further processing
```

#### Without `connexion`, Option 2: Python Type Hinting:
- Utilize Python's type hinting to indicate expected data types.
- Type hints do not enforce type checking at runtime but are useful for static analysis.
- For runtime validation, manual checks or additional libraries like `pydantic` can be employed.

```python
from flask import Flask, jsonify, request
from typing import Any, Dict

app = Flask(__name__)

@app.route('/users/<int:userId>', methods=['GET'])
def get_user(userId: int) -> Dict[str, Any]:
    # Type hinting suggests that userId should be an integer
    # Additional runtime validation can be performed if necessary
    return jsonify({"id": userId, "name": "John Doe"})
```

*Note: While type hints improve code readability and help with development tools, they do not replace runtime validation for ensuring data integrity.*

## 4. Data Serialization/Deserialization

### With `connexion`:
- Serialization and deserialization are automatically handled based on the OpenAPI spec.

### Without `connexion`:
- Manually serialize/deserialize data.

```python
@app.route('/users/<int:userId>', methods=['GET'])
def get_user(userId):
    return jsonify({"id": userId, "name": "John Doe"})
```

---

*This guide is intended to provide a basic comparison and is not exhaustive.*
