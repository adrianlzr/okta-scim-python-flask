import requests, base64, json
from flask import request, Response, render_template
def auth_required(method=None, okta=True):
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
                    return False
                else:
                    return True
            def oauth2(okta):
                jwt = get_header()
                if 'empty' not in jwt:
                    if okta: 
                        is_valid = okta_jwt_remote_validator(jwt)
                    else:
                        ##
                        ## Validator for any other provider will be configured. For now, returning True as default.
                        ##
                        is_valid = True
                else:
                    is_valid = False
                return is_valid
            def okta_jwt_remote_validator(jwt):
                '''
                These lines are commented out for now.
                This will be improved to use ENV Variables.
                
                client_id = "0oa13mjq7j9jacY8M357"
                client_secret = "HmQiJTBhJe46Ezk1nzapp138_8NbNI7aZcZpvJUk"
                creds = client_id + ":" + client_secret
                b64_creds = base64.b64encode(creds.encode()).decode()
                auth_header = "Basic " + b64_creds
                headers = {"Authorization":auth_header}
                token = str(jwt[7:(len(jwt))])
                body = {"token":token}
                response = requests.post("https://adrian.okta.com/oauth2/ausa8dtz9H5QTLpmC356/v1/introspect", data=body, headers=headers)
                response_json = response.json()
                active = response_json["active"]
                '''
                active = True
                return active
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
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

