from core.Database import Database
from models.Group import Group
import json, time

db = Database()
group = Group()

class Groups():

    def __init__(self):
        pass

    def get_group(self, id, req_url):

        result = db.get_group_db(id, req_url)
        return result

    def get_all_groups(self, req_url, start_index, count):
        
        result = db.get_all_groups_db(req_url, start_index, count)
        return result
    
    def get_filtered_groups(self, attribute_name, attribute_value, req_url, start_index, count):
        
        result = db.get_filtered_groups_db(attribute_name, attribute_value, req_url, start_index, count)
        return result

    def create_group(self, group_data_json, req_url):

        group_model = group.ParseFromSCIMResource(group_data_json, req_url)
        result = db.create_group_db(group_model, req_url)
        return result
    
    def update_group(self, group_data_json, req_url):
        pass
        
    def patch_group(self, group_data_json, id, req_url):

        try: 
            path = group_data_json['Operations'][0]['path']
        except KeyError:
            path = None
        operation = group_data_json['Operations'][0]['op']
        value = group_data_json['Operations'][0]['value']
        if operation == 'replace':
            if path:
                i = 0 
                users = []
                while i < len(value):
                    userId = value[i]["value"]
                    i += 1
                    users.append(userId)
                db.patch_group_db_replace(users, id, req_url)
                return self.get_group(id, req_url)            
            if not path:
                for key, val in value.items():
                    attribute_name = key
                    attribute_value = val
                    db.patch_group_db_sync(attribute_name, attribute_value, id, req_url)
                return self.get_group(id, req_url)
               
        if operation == 'add':
            i = 0 
            while i < len(value):
                userId = value[i]["value"]
                i += 1
                db.patch_group_db_add(userId, id)
            return self.get_group(id, req_url)
            
    def delete_group(self, id, req_url):

        delete_group_db = db.delete_group_db(id)
        return self.get_group(id, req_url)
     
        
