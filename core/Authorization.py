from core.SCIMCore import SCIMCore
from flask import request
import base64, time, json
scimCore = SCIMCore()

class Authorization():

    def __init__(self):
        return

    def get_auth_header(self):
        try: 
            headers = request.headers["Authorization"][6:25]
            return headers
        except KeyError:
            statusCode = 401
            errorMessage = "{}".format("No authorization header present in the request.")
            scimError = scimCore.CreateSCIMEerror(errorMessage, statusCode)
            return scimError

                
    
    def require_basic_auth(self, username, password):
        auth_header = self.get_auth_header()
        try:
            if auth_header['status']:
                return auth_header
        except TypeError:
            creds = username+":"+password
            b64_creds = base64.b64encode(creds.encode())
            if auth_header != b64_creds.decode():
               statusCode = 401
               errorMessage = "{}".format("Invalid credentials. Request is unauthorized")
               scimError = scimCore.CreateSCIMEerror(errorMessage, statusCode)
               return scimError