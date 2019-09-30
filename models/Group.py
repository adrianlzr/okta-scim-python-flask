from core.SCIMCore import SCIMCore
import uuid, time

uid = None
scim_core = SCIMCore()

class Group():
    
    def __init__(self):
        pass
    
    def ParseFromSCIMResource(self, group_data_json, req_url):

        group={
            "id":"",
            "displayName":"",
            "members":[]
        }
        try:
            if group_data_json["id"]:
                group["id"] = group_data_json["id"]
        except KeyError:
            uid = str(uuid.uuid4())
            group["id"] = uid
        try:
            if group_data_json['displayName']:
                group["displayName"] = group_data_json['displayName']
        except KeyError:
            status_code = 400
            error_message = "Mandatory attribute - displayName - missing."
            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
            return scim_error
        try:
            if group_data_json["members"]:
                members=[]
                for member in group_data_json["members"]:
                    parsed_member = self.ParseMemberships(member, req_url)
                    members.append(parsed_member)
                group["members"] = members
        except KeyError:
            group["members"] = []
        
        return group

    def ParseMemberships(self, group_members, req_url):
    
        membership = {
            "value":"",
            "ref":"",
            "display":""
        }
        a = len(req_url)
        b = len('/Groups')
        c = (a - b)
        d = req_url[0:c]
        location = d + "/Users/" + group_members["value"]
        membership["value"] = group_members["value"]
        membership["ref"] = location
        #membership["display"] = group_members["display"]
        location = ''
        
        return membership