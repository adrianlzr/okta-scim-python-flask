from core.SCIMCore import SCIMCore
scim_core = SCIMCore()

class User():
    def __init__(self):
        return 
    
    def ParseFromSCIMResource(self,user_data_json):

        user = {
            "active": False,
            "userName":'',
            "givenName":'',
            "middleName":'',
            "familyName":'',
            "email":'',
            "groups":''
        }

        user["active"] = True
        #userName
        try:
            if user_data_json['userName']:
                user["userName"] = user_data_json['userName']
        except KeyError:
            status_code = 400
            error_message = "Mandatory attribute - userName - missing."
            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
            return scim_error 
        #givenName        
        try:
            if user_data_json['name']['givenName']:
                user['givenName'] = user_data_json['name']['givenName']
        except KeyError:
            try:
                if user_data_json['givenName']:
                    user["givenName"] = user_data_json['givenName']
            except KeyError:
                status_code = 400
                error_message = "Mandatory attribute - givenName - missing."
                scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
                return scim_error
        #middleName                                              
        try:
            if user_data_json['name']['middleName']:
                user['middleName'] = user_data_json['name']['middleName']
        except KeyError:
            try:
                if user_data_json['middleName']:
                    user["middleName"] = user_data_json['middleName']
            except KeyError:
                user['middleName'] = ''
                pass
        #familyName           
        try:
            if user_data_json['name']['familyName']:
                user['familyName'] = user_data_json['name']['familyName']
        except KeyError:
            try:
                if user_data_json['familyName']:
                    user["familyName"] = user_data_json['familyName']
            except KeyError:
                status_code = 400
                error_message = "Mandatory attribute - familyName - missing."
                scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
                return scim_error
        #email   
        try:
            if user_data_json['emails'][0]['value']:
                user['email'] = user_data_json['emails'][0]['value']
        except KeyError:
            try:
                if user_data_json['email']:
                    user["email"] = user_data_json['email']
            except KeyError:
                status_code = 400
                error_message = "Mandatory attribute - email - missing."
                scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
                return scim_error
        #groups  
        try:
            if user_data_json['groups']:
                user["groups"] = user_data_json['groups']
        except KeyError:
            user['groups'] = ''
            
        return user        
