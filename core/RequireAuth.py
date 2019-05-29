import base64, time
from flask import request, Response, render_template
def auth_required(method=None):
    def decorator(f):
        def wrapper(*args, **kwargs):
            def get_header():
                auth_header = request.headers.get("Authorization")
                if auth_header and 'Basic' in auth_header:
                    auth_header = auth_header[6:25]
                elif auth_header and 'Bearer' in auth_header:
                    auth_header = auth_header
                return auth_header
            def basic_auth(username, password):
                auth_header = get_header()
                creds = username+":"+password
                b64_creds = base64.b64encode(creds.encode())
                if auth_header != b64_creds.decode():
                    return Response(render_template("403.html"), status=403, mimetype="text/html")
            def oauth2():
                auth_header = get_header()
                if 'Bearer' not in auth_header:
                    return Response(render_template("403.html"), status=403, mimetype="text/html")
            if method == 'basic_auth':
                auth = basic_auth("user", "p@ss")
                if auth is None:
                    return f(*args, **kwargs)
                else:
                    return auth
            if method == 'oauth2':
                auth = oauth2()
                if auth is None:
                    return f(*args, **kwargs)
                else:
                    return auth
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

