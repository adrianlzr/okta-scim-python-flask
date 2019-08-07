import mysql.connector
from core.SCIMCore import SCIMCore
import uuid
import time
uid = None

mydb = mysql.connector.connect(host='localhost', user='root' , database='scim')
mycursor = mydb.cursor()
scim_core = SCIMCore()


class Database():

    global mydb, mycursor

    def __init__(self):
        mycursor.execute("SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_NAME='Users' and TABLE_SCHEMA='scim'")
        myresult = mycursor.fetchall()
        if not myresult:
            mycursor.execute("CREATE TABLE IF NOT EXISTS `Users` (`id` varchar(255) COLLATE utf8_general_ci NOT NULL,`active` int(11) NOT NULL,`userName` varchar(255) COLLATE utf8_general_ci NOT NULL,`givenName` varchar(255) COLLATE utf8_general_ci NOT NULL,`middleName` varchar(255) COLLATE utf8_general_ci NOT NULL,`familyName` varchar(255) COLLATE utf8_general_ci NOT NULL,`email` varchar(255) COLLATE utf8_general_ci NOT NULL,`password` varchar(255) COLLATE utf8_general_ci, PRIMARY KEY (`id`)) ENGINE = MyISAM;")

        mycursor.execute("SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_NAME='Groups' and TABLE_SCHEMA='scim'")
        myresult = mycursor.fetchall()
        if not myresult:
            mycursor.execute("CREATE TABLE IF NOT EXISTS `Groups` ( `id` VARCHAR(255) COLLATE utf8_general_ci NOT NULL , `displayName` VARCHAR(255) COLLATE utf8_general_ci NOT NULL , PRIMARY KEY (`id`)) ENGINE = MyISAM;")

        mycursor.execute("SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_NAME='GroupMembershups' and TABLE_SCHEMA='scim'")
        myresult = mycursor.fetchall()
        if not myresult:
            mycursor.execute("CREATE TABLE IF NOT EXISTS `GroupMemberships` (`Id` varchar(255) COLLATE utf8_general_ci NOT NULL,`groupId` varchar(255) COLLATE utf8_general_ci NOT NULL,`userId` varchar(255) COLLATE utf8_general_ci NOT NULL, PRIMARY KEY (`Id`)) ENGINE=MyISAM;")

    def get_user_db(self, id, req_url):

        try:
            mycursor.execute("SELECT * FROM `Users` WHERE id='{}'".format(id))
        except mysql.connector.Error as err:
            status_code = 400
            error_message = "{}".format(err)
            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
            return scim_error 
        myresult = mycursor.fetchall()
        if myresult:
            row = [list(i) for i in myresult][0]
            userId = row[0]
            groups = self.get_groups_for_user(userId, req_url)
            row.append(groups)
            return scim_core.ParseSCIMUser(row, req_url)            
        else:
            status_code = 404
            error_message = "Not found."
            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
            return scim_error

    def get_all_users_db(self, req_url, start_index, count):

        start_index = int(start_index)
        count = int(count)

        try:
            mycursor.execute("SELECT * FROM `Users` LIMIT {}, {}".format((start_index-1), count))
        except mysql.connector.Error as err:
            status_code = 400
            error_message = "{}".format(err)
            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
            return scim_error
        myresults = mycursor.fetchall()
        rows = [list(i) for i in myresults]
        for row in rows:
            userId = row[0]
            groups = self.get_groups_for_user(userId, req_url)
            row.append(groups)     
        total_results = 0
        try:
            mycursor.execute("SELECT * from `Users`")
        except mysql.connector.Error as err:
            status_code = 400
            error_message = "{}".format(err)
            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
            return scim_error
        myresults = mycursor.fetchall()
        for row in myresults:
            total_results += 1
        return scim_core.CreateSCIMUserList(start_index, count, total_results, req_url, rows)
    
    def get_filtered_users_db(self, req_url, attribute_name, attribute_value, start_index, count):

        start_index = int(start_index)
        count = int(count)
        try:
            mycursor.execute("SELECT * FROM `Users` WHERE {} = '{}' LIMIT {}, {}".format(attribute_name, attribute_value, (start_index-1), count))
        except mysql.connector.Error as err:
            status_code = 400
            error_message = "{}".format(err)
            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
            return scim_error
        myresults = mycursor.fetchall()
        rows = [list(i) for i in myresults]
        for row in rows:
            userId = row[0]
            groups = self.get_groups_for_user(userId, req_url)
            row.append(groups)
        total_results = 0
        try:
            mycursor.execute("SELECT * from `Users`")
        except mysql.connector.Error as err:
            status_code = 400
            error_message = "{}".format(err)
            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
            return scim_error
        myresults = mycursor.fetchall()
        for row in myresults:
            total_results += 1
        return scim_core.CreateSCIMUserList(start_index, count, total_results, req_url, rows)
    
    def get_groups_for_user(self, id, req_url):
        try:
            mycursor.execute("SELECT * from `GroupMemberships` WHERE userId = '{}'".format(id))
        except mysql.connector.Error as err:
            status_code = 400
            error_message = "{}".format(err)
            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
            return scim_error
        myresults = mycursor.fetchall()
        groups_for_user = []
        if myresults:
            rows = [list(i) for i in myresults]
            for group in rows:
                groups_dict = {
                    "value":"",
                    "ref":"",
                    "display":""
                }                
                groupId = group[1]
                groups_dict["value"] = groupId
                mycursor.execute("SELECT * FROM `Groups` WHERE id='{}'".format(groupId))
                get_groupName = mycursor.fetchall()
                if get_groupName:
                    groupName = [list(i) for i in get_groupName][0][1]
                    groups_dict["display"] = groupName
                    a = len(req_url)
                    b = len('/Users/'+id)
                    e = len('/Users')
                    #c = len(req_url+"/"+id)
                    if id in req_url:
                        c = (a - b)
                        d = req_url[0:c]
                        location = d + "/Groups/" + groupId
                    else:
                        c = (a - e)
                        d = req_url[0:c]
                        location = d + "/Groups/" + groupId
                    groups_dict["ref"] = location                   
                    groups_for_user.append(groups_dict)
            return groups_for_user                           

    def create_user_db(self, user_model, req_url):
        
        try:
            mycursor.execute("SELECT * FROM `Users` WHERE userName='{}'".format(user_model['userName']))
        except mysql.connector.Error as err:
            status_code = 400
            error_message = "{}".format(err)
            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
            return scim_error
        
        myresult = mycursor.fetchall()

        if myresult == []:
            uid = str(uuid.uuid4())
            req_url = req_url+'/'+uid
            sql = "INSERT INTO `Users` (id, active, userName, givenName, middleName, familyName, email) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (uid, user_model['active'], user_model['userName'], user_model['givenName'], user_model['middleName'], user_model['familyName'], user_model['email'])
            try: 
                mycursor.execute(sql, val)
            except mysql.connector.Error as err:
                status_code = 400
                error_message = "{}".format(err)
                scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
                return scim_error
            #scim_core.CreateSCIMUser(uid, True, user_model['userName'], user_model['givenName'], user_model['familyName'], user_model['email'], req_url, user_model['middleName'], user_model['groups'])
            if user_model["groups"] != []:
                for group in user_model["groups"]:
                    groupId = group["value"]
                    self.patch_group_db_add(uid, groupId)
                return self.get_user_db(uid, req_url)
            else:
                return self.get_user_db(uid, req_url)
        else: 
            for row in myresult:
                row = [list(i) for i in myresult]
                row = row[0]
                row = row[2]
            if row == user_model['userName']:
                status_code = 409
                error_message = "Conflict! User already exists"
                scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
                return scim_error

    def update_user_db(self, user_model, id, req_url):
        
        try:
            mycursor.execute("SELECT * FROM `Users` WHERE id='{}'".format(id))
        except mysql.connector.Error as err:
            status_code = 400
            error_message = "{}".format(err)
            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
            return scim_error
        
        myresult = mycursor.fetchall()

        if myresult == []:
            status_code = 404
            error_message = "User not found."
            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
            return scim_error            
        else: 
            try:
                mycursor.execute("UPDATE Users SET userName='{}', givenName='{}', middleName='{}', familyName='{}', email='{}' WHERE id='{}'".format(user_model['userName'], user_model['givenName'], user_model['middleName'], user_model['familyName'], user_model['email'], id))
            except mysql.connector.Error as err:
                status_code = 400
                error_message = "{}".format(err)
                scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
                return scim_error
            #updatedUser = scim_core.CreateSCIMUser(id, True, user_model['userName'], user_model['givenName'], user_model['familyName'], user_model['email'], req_url, user_model['middleName'], user_model['groups'])
            if user_model["groups"] != []:
                for group in user_model["groups"]:
                    groupId = group["value"]
                    self.patch_group_db_add(id, groupId)
                return self.get_user_db(id, req_url)
            else:
                return self.get_user_db(id, req_url)
    
    def patch_user_db(self, attribute_name, attribute_value, id, req_url):

        try:
            mycursor.execute("UPDATE Users SET {}='{}' WHERE id='{}'".format(attribute_name, attribute_value, id))
        except mysql.connector.Error as err:
            status_code = 400
            error_message = "{}".format(err)
            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
            return scim_error              

        try:
            mycursor.execute("SELECT * From `Users` WHERE id='{}'".format(id))
        except mysql.connector.Error as err:
            status_code = 400
            error_message = "{}".format(err)
            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
            return scim_error
        myresult = mycursor.fetchall()
        if myresult == []:
            status_code = 404
            error_message = "User not found."
            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
            return scim_error            
        else:
            return self.get_user_db(id, req_url)
            #row = [list(i) for i in myresult][0]
            #patchedUser = scim_core.ParseSCIMUser(row, req_url)
            #return patchedUser

    def get_group_db(self, id, req_url):

        try:
            mycursor.execute("SELECT * from `Groups` WHERE id='{}'".format(id))
        except mysql.connector.Error as err:
            status_code = 400
            error_message = "{}".format(err)
            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
            return scim_error
        myresult = mycursor.fetchall()
        if myresult:
            row = [list(i) for i in myresult][0]
            members = self.get_users_for_group_db(id, req_url)
            return scim_core.ParseSCIMGroup(row, req_url, members)
        else:
            status_code = 404
            error_message = "Group not found."
            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
            return scim_error
  
    def get_all_groups_db(self, req_url, start_index, count):

        start_index = int(start_index)
        count = int(count)        
        try:
            mycursor.execute("SELECT * from `Groups` LIMIT {}, {}".format((start_index-1), count))
        except mysql.connector.Error as err:
            status_code = 400
            error_message = "{}".format(err)
            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
            return scim_error
        myresults = mycursor.fetchall()
        rows = [list(i) for i in myresults]
        for row in rows:
            groupId = row[0]
            members = self.get_users_for_group_db(groupId, req_url)
            if members:
                row.append(members)
        total_results = 0
        try:
            mycursor.execute("SELECT * from `Groups`")
        except mysql.connector.Error as err:
            status_code = 400
            error_message = "{}".format(err)
            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
            return scim_error
        myresults = mycursor.fetchall()
        for row in myresults:
            total_results += 1
        return scim_core.CreateSCIMGroupList(start_index, count, total_results, req_url, rows)

    def get_filtered_groups_db(self, attribute_name, attribute_value, req_url, start_index, count):

        start_index = int(start_index)
        count = int(count)
        try:
            mycursor.execute("SELECT * from `Groups` WHERE {} = '{}' LIMIT {}, {}".format(attribute_name, attribute_value, (start_index-1), count))
        except mysql.connector.Error as err:
            status_code = 400
            error_message = "{}".format(err)
            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
            return scim_error
        myresults = mycursor.fetchall()
        rows = [list(i) for i in myresults]
        for row in rows:
            groupId = row[0]
            members = self.get_users_for_group_db(groupId, req_url)
            row.append(members)
        total_results = 0
        try:
            mycursor.execute("SELECT * from `Groups`")
        except mysql.connector.Error as err:
            status_code = 400
            error_message = "{}".format(err)
            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
            return scim_error
        myresults = mycursor.fetchall()
        for row in myresults:
            total_results += 1
        return scim_core.CreateSCIMGroupList(start_index, count, total_results, req_url, rows)

    def get_users_for_group_db(self, id, req_url):
        try:
            mycursor.execute("SELECT * from `GroupMemberships` WHERE groupId = '{}'".format(id))
        except mysql.connector.Error as err:
            status_code = 400
            error_message = "{}".format(err)
            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
            return scim_error
        myresults = mycursor.fetchall()
        users_for_group = []
        if myresults:
            rows = [list(i) for i in myresults]
            for user in rows:
                users_dict = {
                    "value":"",
                    "ref":"",
                    "display":""
                }                
                userId = user[2]
                users_dict["value"] = userId
                mycursor.execute("SELECT * FROM `Users` WHERE id='{}'".format(userId))
                get_userName = mycursor.fetchall()
                if get_userName:
                    userName = [list(i) for i in get_userName][0][2]
                    users_dict["display"] = userName
                    a = len(req_url)
                    b = len('/Groups/'+id)
                    e = len('/Groups')
                    #c = len(req_url+"/"+id)
                    if id in req_url:
                        c = (a - b)
                        d = req_url[0:c]
                        location = d + "/Users/" + userId
                    else:
                        c = (a - e)
                        d = req_url[0:c]
                        location = d + "/Users/" + userId
                    users_dict["ref"] = location                   
                    users_for_group.append(users_dict)
            return users_for_group                      
        else: 
            return users_for_group

              

    def create_group_db(self, group_model, req_url):

        try:
            mycursor.execute("SELECT * FROM `Groups` WHERE displayName = '{}'".format(group_model["displayName"]))
        except mysql.connector.Error as err:
            status_code = 400
            error_message = "{}".format(err)
            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
            return scim_error
        myresult = mycursor.fetchall()
        if not myresult:
            try:
                sql = "INSERT INTO `Groups` (id, displayName) VALUES(%s, %s)"
                val = (group_model["id"], group_model["displayName"])
                mycursor.execute(sql, val)
            except mysql.connector.Error as err:
                status_code = 400 
                error_message = "{}".format(err)
                scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
                return scim_error
            groupId = group_model["id"]
            group_location = req_url + "/" + group_model["id"]
            members = group_model["members"] 
            if members:
                for member in members:
                    userId = member["value"]
                    self.patch_group_db_add(userId, groupId)
            return self.get_group_db(group_model["id"], group_location)
        if myresult:
            status_code = 409
            error_message = "Conflict! Group already exists"
            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
            return scim_error            

    def update_group_db(self):
        pass

    def patch_group_db_sync(self, attribute_name, attribute_value, id, req_url):

        try:
            mycursor.execute("UPDATE `Groups` SET `{}` = '{}' WHERE `id` = '{}' ".format(attribute_name, attribute_value, id))
        except mysql.connector.Error as err:
            status_code = 400
            error_message = "{}".format(err)
            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
            return scim_error
        

    def patch_group_db_add(self, userId, groupId):

        try:
            mycursor.execute("SELECT * FROM `GroupMemberships` WHERE groupId = '{}' AND userId = '{}'".format(groupId, userId))
        except mysql.connector.Error as err:
            status_code = 400
            error_message = "{}".format(err)
            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
            return scim_error
        myresult = mycursor.fetchall()
        if not myresult:
            uid = str(uuid.uuid4())
            try:
                sql = "INSERT INTO `GroupMemberships` (Id, groupId, userId) VALUES(%s, %s, %s)"
                val = (uid, groupId, userId)
                mycursor.execute(sql, val)
            except mysql.connector.Error as err:
                status_code = 400
                error_message = "{}".format(err)
                scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
                return scim_error
        else:
            status_code = 409
            error_message = "Conflict! Group membership already exists."
            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
            return scim_error
    
    def patch_group_db_replace(self, users, id, req_url):        
        try:
            mycursor.execute("SELECT * FROM `GroupMemberships` WHERE groupId = '{}'".format(id))
        except mysql.connector.Error as err:
            status_code = 400
            error_message = "{}".format(err)
            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
            return scim_error
        myresults = mycursor.fetchall()
        rows = [list(i) for i in myresults]
        for row in rows:
            if row[2] not in users:
                try:
                    mycursor.execute("DELETE FROM `GroupMemberships` WHERE Id = '{}'".format(row[0]))
                except mysql.connector.Error as err:
                    status_code = 400
                    error_message = "{}".format(err)
                    scim_error = scim_core.CreateSCIMEerror(error_message, status_code)
                    return scim_error
            

    def delete_group_db(self, groupId):
        try:
            mycursor.execute("DELETE FROM `Groups` WHERE id = '{}'".format(groupId))
            mycursor.execute("DELETE FROM `GroupMemberships` WHERE groupId = '{}'".format(groupId))
        except mysql.connector.Error as err:
            status_code = 400
            error_message = "{}".format(err)
            scim_error = scim_core.CreateSCIMError(error_message, status_code)
            return scim_error
