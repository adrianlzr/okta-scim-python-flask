import base64, time
from flask import request, Response, render_template
def auth_required():
    def decorator(f):
        def wrapper(*args, **kwargs):
            def get_header():
                auth_header = request.headers.get("Authorization")
                if auth_header:
                    auth_header = auth_header[6:25]
                return auth_header
            def basic_auth(username, password):
                auth_header = get_header()
                creds = username+":"+password
                b64_creds = base64.b64encode(creds.encode())
                if auth_header != b64_creds.decode():
                    return Response(render_template("403.html"), status=403, mimetype="text/html")
            auth = basic_auth("user", "p@ss")
            if auth is None:
                return f(*args, **kwargs)
            else:
                return auth
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

