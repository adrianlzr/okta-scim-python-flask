class SCIMCore():

    def __init__(self):
        return 

    def CreateSCIMUser(self, id, active, userName, givenName, familyName, email, req_url, middleName=None, groups=None): 
        scim_user = {
            "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
            "id": "",
            "externalId":"TBA",
            "userName":"",
            "name":{
                "givenName":"",
                "middleName":"",
                "familyName":"",
            },
            "displayName": "",
            "nickName":"",
            "profileUrl":"",
            "emails":[{
                "primary":True,
                "value":"",
                "type":"work"
            }],
            "active":False,
            "groups":[],
            "meta":{
                "resourceType":"User",
                "created":"TBA",
                "lastModified":"TBA",
                "location":""
            }
        }
        if active == 1:
            scim_user["active"]=True
        else:
            scim_user["active"]=False
        scim_user["id"] = id
        scim_user["userName"] = userName
        scim_user["name"]["givenName"] = givenName
        if middleName:
            scim_user["name"]["middleName"] = middleName
        else:
            middleName = None
        scim_user["name"]["familyName"] = familyName
        scim_user["displayName"] = givenName + " " + familyName
        scim_user["emails"][0]["value"] = email
        if groups:
            scim_user["groups"]=groups
        scim_user["meta"]["location"] = req_url
        scim_user["profileUrl"] = req_url
        return scim_user

    def ParseSCIMUser(self, row, req_url, groups=None):
        if groups:
            return self.CreateSCIMUser(row[0], row[1], row[2], row[3], row[5], row[6], req_url, row[4], groups)
        else:
            try: 
                groups = row[8]
                return self.CreateSCIMUser(row[0], row[1], row[2], row[3], row[5], row[6], req_url, row[4], row[8])
            except IndexError:
                return self.CreateSCIMUser(row[0], row[1], row[2], row[3], row[5], row[6], req_url, row[4])

    def CreateSCIMUserList(self, startIndex, count, totalResults, req_url, rows=None, groups=None):
        scim_resources = {
            "Resources": [],
            "itemsPerPage": 0,
            "schemas":["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
            "startIndex": 0
        }
        resources = []
        if not rows:
            scim_resources["Resources"] = resources
        else:
            if rows:
                for row in rows:
                    location = str(req_url)+"/"+row[0]
                    resource = self.ParseSCIMUser(row, location)
                    resources.append(resource)
                    location = ""
            scim_resources["Resources"] = resources
        if totalResults > 0:
            scim_resources["itemsPerPage"] = count
        else:
            scim_resources["itemsPerPage"] = 0
        if totalResults > 0:
            scim_resources["startIndex"] = startIndex
        else:
            scim_resources["startIndex"] = 0
        if scim_resources["Resources"] != []:
            scim_resources["totalResults"] = totalResults
        else:
            scim_resources["totalResults"] = 0
        return scim_resources
    
    def CreateSCIMGroup(self, id, displayName, req_url, group_location=None, members=None):
        scim_group = {
			"schemas":[],
			"id":"",
			"displayName":"",
			"members":[],
			"meta":{
				"resourceType":"Group",
				"location":""
            }
        }
        schemas = ["urn:ietf:params:scim:schemas:core:2.0:Group"]
        scim_group["schemas"] = schemas
        scim_group["id"] = id
        scim_group["displayName"] = displayName
        if members:
            scim_group["members"] = members
        else:
            scim_group["members"] = []
        if group_location:
            scim_group["meta"]["location"] = group_location
        else:
            scim_group["meta"]["location"] = req_url
        return scim_group

    def ParseSCIMGroup(self, row, req_url, members=None, group_location=None):
        if members: 
            return self.CreateSCIMGroup(row[0], row[1], req_url, group_location, members)
        else:
            try:
                if row[2]:
                    return self.CreateSCIMGroup(row[0], row[1], req_url, group_location, row[2])
            except IndexError:
                return self.CreateSCIMGroup(row[0], row[1], req_url, group_location)
            


    def CreateSCIMGroupList(self, startIndex, count, totalResults, req_url, rows=None, members=None):
        scim_resources = {
            "Resources": [],
            "itemsPerPage": 0,
            "schemas":["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
            "startIndex": 0
        }
        resources = []
        if not rows:
            scim_resources["Resources"] = resources

        else:
            if rows:
                for row in rows:
                    location = str(req_url)+"/"+row[0]
                    resource = self.ParseSCIMGroup(row, location, members)
                    resources.append(resource)
                    location = ""
            scim_resources["Resources"] = resources
        if totalResults > 0:
            scim_resources["itemsPerPage"] = count
        else:
            scim_resources["itemsPerPage"] = 0
        if totalResults > 0:
            scim_resources["startIndex"] = startIndex
        else:
            scim_resources["startIndex"] = 0
        scim_resources["totalResults"] = totalResults   
        return scim_resources

    def CreateSCIMEerror(self, error_message, status_code):
        scim_error = {
            "schemas":["urn:ietf:params:scim:api:messages:2.0:Error"],
            "detail":None,
            "status":None
        }
        scim_error["detail"] = error_message
        scim_error["status"] = status_code
        return scim_error