from flask import request, Response

def read_file():
    binary_content = request.data
    # Convert the binary content to string (assuming utf-8 encoding here)
    content_str = binary_content.decode('utf-8')
    return Response(content_str, content_type='text/plain')