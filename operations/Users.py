from core.Database import Database
from models.User import User
import json, time

db = Database()
user = User()

class Users():
    def __init__(self):
        pass
    
    def get_user(self, id, req_url):

        result = db.get_user_db(id, req_url)
        return result

    def get_all_users(self, req_url, start_index, count):

        result = db.get_all_users_db(req_url, start_index, count)
        return result

    def get_filtered_users(self, req_url, attribute_name, attribute_value, start_index, count):
        
        result = db.get_filtered_users_db(req_url, attribute_name, attribute_value, start_index, count)
        return result

    def create_user(self, user_data_json, req_url):

        user_model = user.ParseFromSCIMResource(user_data_json)
        result = db.create_user_db(user_model, req_url)
        return result

    def update_user(self, user_data_json, id, req_url):

        user_model = user.ParseFromSCIMResource(user_data_json)
        result = db.update_user_db(user_model, id, req_url)
        return result
    
    def patch_user(self, user_data_json, id, req_url):

        operation = user_data_json['Operations'][0]['op']
        if operation == 'replace':
            value = user_data_json['Operations'][0]['value']
            for key in value:
                attribute_name = key
                attribute_value = value[key]
            if attribute_value == True:
                attribute_value = 1
            elif attribute_value == False:
                attribute_value = 0
            result = db.patch_user_db(attribute_name, attribute_value, id, req_url)
            return result