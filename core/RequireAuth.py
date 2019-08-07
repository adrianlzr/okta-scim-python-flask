import requests, base64, json
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
                elif not auth_header:
                    auth_header = 'empty'
                return auth_header
            def basic_auth(username, password):
                auth_header = get_header()
                creds = username+":"+password
                b64_creds = base64.b64encode(creds.encode())
                if auth_header != b64_creds.decode():
                    return Response(render_template("403.html"), status=403, mimetype="text/html")
            def oauth2():
                auth_header = get_header()
                is_valid = verify_jwt(auth_header)
                return is_valid
            def verify_jwt(jwt):
                client_id = "0oal5v65arFcwMlBr0h7"
                client_secret = "RCXRQKx7-q5JiCWXx9zTNtFi6RT0XMYZ_NVMMgyb"
                creds = client_id + ":" + client_secret
                b64_creds = base64.b64encode(creds.encode()).decode()
                auth_header = "Basic " + b64_creds
                headers = {"Authorization":auth_header}
                token = str(jwt[7:(len(jwt))])
                body = {"token":token}
                response = requests.post("https://adrian.oktapreview.com/oauth2/ausmsd6ln3STtnTxo0h7/v1/introspect", data=body, headers=headers)
                response_json = response.json()
                active = response_json["active"]
                return active
            if method == 'basic_auth':
                auth = basic_auth("user", "p@ss")
                if auth is None:
                    return f(*args, **kwargs)
                else:
                    return auth
            if method == 'oauth2':
                auth = oauth2()
                if auth == True:
                    return f(*args, **kwargs)
                else:
                    return Response(render_template("403.html"), status=403, mimetype="text/html")
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

