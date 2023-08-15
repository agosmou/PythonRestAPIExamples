from flask import request, Response

def read_file():
    binary_content = request.data
    # Convert the binary content to string (assuming utf-8 encoding here)
    content_str = binary_content.decode('utf-8')
    return Response(content_str, content_type='text/plain')

def typecast(a_string: str, an_integer: int, a_float: float, a_boolean: bool):
    if not isinstance(a_string, str):
        raise TypeError("Parameter 'a_string' should be of type string.")
    
    if not isinstance(an_integer, int):
        raise TypeError("Parameter 'an_integer' should be of type integer.")
    
    if not isinstance(a_float, float):
        raise TypeError("Parameter 'a_float' should be of type float.")
    
    if not isinstance(a_boolean, bool):
        raise TypeError("Parameter 'a_boolean' should be of type boolean.")
    
    return "Parameters received and types are correct."