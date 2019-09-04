import requests, base64, json
from flask import request, Response, render_template
from py_jwt_validator import PyJwtValidator, PyJwtException


def auth_required(method=None, okta=True):
    def decorator(f):
        def wrapper(*args, **kwargs):
            def get_header():
                auth_header = request.headers.get("Authorization")
                if auth_header and 'Basic' in auth_header:
                    auth_header = auth_header[6:25]
                elif auth_header and 'Bearer ' in auth_header:
                    auth_header = auth_header[len('Bearer '):len(auth_header)]
                elif not auth_header:
                    auth_header = 'empty'
                return auth_header
            def basic_auth(username, password):
                auth_header = get_header()
                creds = username+":"+password
                b64_creds = base64.b64encode(creds.encode())
                if auth_header != b64_creds.decode():
                    return False
                else:
                    return True
            def oauth2(okta):
                jwt = get_header()
                if 'empty' not in jwt:
                    if okta: 
                        is_valid = okta_jwt_local_validator(jwt)
                    else:
                        ##
                        ## Validator for any other provider will be configured. For now, returning True as default.
                        ##
                        is_valid = True
                else:
                    is_valid = False
                return is_valid
            def okta_jwt_local_validator(jwt):
                try:
                    verify = PyJwtValidator(jwt)
                    return True
                except PyJwtException:
                    return False
            if method == 'basic_auth':
                auth = basic_auth("user", "p@ss")
                if auth == True:
                    return f(*args, **kwargs)
                else:
                    return Response(render_template("403.html"), status=403, mimetype="text/html")
            if method == 'oauth2':
                auth = oauth2(okta)
                if auth == True:
                    return f(*args, **kwargs)
                else:
                    return Response(render_template("403.html"), status=403, mimetype="text/html")
            if method is None:
                return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

