[33mcommit 2bed9f9c65d8defc1f74bcbe17509f37d3c78960[m[33m ([m[1;36mHEAD -> [m[1;32mmaster[m[33m)[m
Author: Adrian Lazar <adrian.lazar@okta.com>
Date:   Tue May 28 12:47:48 2019 +0300

    Initial commit

[1mdiff --git a/__pycache__/cors.cpython-36.pyc b/__pycache__/cors.cpython-36.pyc[m
[1mnew file mode 100644[m
[1mindex 0000000..4905488[m
Binary files /dev/null and b/__pycache__/cors.cpython-36.pyc differ
[1mdiff --git a/__pycache__/db.cpython-36.pyc b/__pycache__/db.cpython-36.pyc[m
[1mnew file mode 100644[m
[1mindex 0000000..872df46[m
Binary files /dev/null and b/__pycache__/db.cpython-36.pyc differ
[1mdiff --git a/__pycache__/flask-scim.cpython-36.pyc b/__pycache__/flask-scim.cpython-36.pyc[m
[1mnew file mode 100644[m
[1mindex 0000000..cd82e2a[m
Binary files /dev/null and b/__pycache__/flask-scim.cpython-36.pyc differ
[1mdiff --git a/__pycache__/lazar_cors.cpython-36.pyc b/__pycache__/lazar_cors.cpython-36.pyc[m
[1mnew file mode 100644[m
[1mindex 0000000..d5a34b3[m
Binary files /dev/null and b/__pycache__/lazar_cors.cpython-36.pyc differ
[1mdiff --git a/__pycache__/server.cpython-36.pyc b/__pycache__/server.cpython-36.pyc[m
[1mnew file mode 100644[m
[1mindex 0000000..74a7e1e[m
Binary files /dev/null and b/__pycache__/server.cpython-36.pyc differ
[1mdiff --git a/__pycache__/test.cpython-36.pyc b/__pycache__/test.cpython-36.pyc[m
[1mnew file mode 100644[m
[1mindex 0000000..221458d[m
Binary files /dev/null and b/__pycache__/test.cpython-36.pyc differ
[1mdiff --git a/core/Authorization.py b/core/Authorization.py[m
[1mnew file mode 100644[m
[1mindex 0000000..dcb8c29[m
[1m--- /dev/null[m
[1m+++ b/core/Authorization.py[m
[36m@@ -0,0 +1,35 @@[m
[32m+[m[32mfrom core.SCIMCore import SCIMCore[m
[32m+[m[32mfrom flask import request[m
[32m+[m[32mimport base64, time, json[m
[32m+[m[32mscimCore = SCIMCore()[m
[32m+[m
[32m+[m[32mclass Authorization():[m
[32m+[m
[32m+[m[32m    def __init__(self):[m
[32m+[m[32m        return[m
[32m+[m
[32m+[m[32m    def get_auth_header(self):[m
[32m+[m[32m        try:[m[41m [m
[32m+[m[32m            headers = request.headers["Authorization"][6:25][m
[32m+[m[32m            return headers[m
[32m+[m[32m        except KeyError:[m
[32m+[m[32m            statusCode = 401[m
[32m+[m[32m            errorMessage = "{}".format("No authorization header present in the request.")[m
[32m+[m[32m            scimError = scimCore.CreateSCIMEerror(errorMessage, statusCode)[m
[32m+[m[32m            return scimError[m
[32m+[m
[32m+[m[41m                [m
[32m+[m[41m    [m
[32m+[m[32m    def require_basic_auth(self, username, password):[m
[32m+[m[32m        auth_header = self.get_auth_header()[m
[32m+[m[32m        try:[m
[32m+[m[32m            if auth_header['status']:[m
[32m+[m[32m                return auth_header[m
[32m+[m[32m        except TypeError:[m
[32m+[m[32m            creds = username+":"+password[m
[32m+[m[32m            b64_creds = base64.b64encode(creds.encode())[m
[32m+[m[32m            if auth_header != b64_creds.decode():[m
[32m+[m[32m               statusCode = 401[m
[32m+[m[32m               errorMessage = "{}".format("Invalid credentials. Request is unauthorized")[m
[32m+[m[32m               scimError = scimCore.CreateSCIMEerror(errorMessage, statusCode)[m
[32m+[m[32m               return scimError[m
\ No newline at end of file[m
[1mdiff --git a/core/Database.py b/core/Database.py[m
[1mnew file mode 100644[m
[1mindex 0000000..27a9569[m
[1m--- /dev/null[m
[1m+++ b/core/Database.py[m
[36m@@ -0,0 +1,492 @@[m
[32m+[m[32mimport mysql.connector[m
[32m+[m[32mfrom core.SCIMCore import SCIMCore[m
[32m+[m[32mimport uuid[m
[32m+[m[32mimport time[m
[32m+[m[32muid = None[m
[32m+[m
[32m+[m[32mmydb = mysql.connector.connect(host='localhost', user='root', database='scim')[m
[32m+[m[32mmycursor = mydb.cursor()[m
[32m+[m[32mscim_core = SCIMCore()[m
[32m+[m
[32m+[m
[32m+[m[32mclass Database():[m
[32m+[m
[32m+[m[32m    global mydb, mycursor[m
[32m+[m
[32m+[m[32m    def __init__(self):[m
[32m+[m[32m        mycursor.execute("SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_NAME='Users' and TABLE_SCHEMA='scim'")[m
[32m+[m[32m        myresult = mycursor.fetchall()[m
[32m+[m[32m        if not myresult:[m
[32m+[m[32m            mycursor.execute("CREATE TABLE IF NOT EXISTS `Users` (`id` varchar(255) COLLATE utf8_general_ci NOT NULL,`active` int(11) NOT NULL,`userName` varchar(255) COLLATE utf8_general_ci NOT NULL,`givenName` varchar(255) COLLATE utf8_general_ci NOT NULL,`middleName` varchar(255) COLLATE utf8_general_ci NOT NULL,`familyName` varchar(255) COLLATE utf8_general_ci NOT NULL,`email` varchar(255) COLLATE utf8_general_ci NOT NULL,`password` varchar(255) COLLATE utf8_general_ci, PRIMARY KEY (`id`)) ENGINE = MyISAM;")[m
[32m+[m
[32m+[m[32m        mycursor.execute("SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_NAME='Groups' and TABLE_SCHEMA='scim'")[m
[32m+[m[32m        myresult = mycursor.fetchall()[m
[32m+[m[32m        if not myresult:[m
[32m+[m[32m            mycursor.execute("CREATE TABLE IF NOT EXISTS `Groups` ( `id` VARCHAR(255) COLLATE utf8_general_ci NOT NULL , `displayName` VARCHAR(255) COLLATE utf8_general_ci NOT NULL , PRIMARY KEY (`id`)) ENGINE = MyISAM;")[m
[32m+[m
[32m+[m[32m        mycursor.execute("SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_NAME='GroupMembershups' and TABLE_SCHEMA='scim'")[m
[32m+[m[32m        myresult = mycursor.fetchall()[m
[32m+[m[32m        if not myresult:[m
[32m+[m[32m            mycursor.execute("CREATE TABLE IF NOT EXISTS `GroupMemberships` (`Id` varchar(255) COLLATE utf8_general_ci NOT NULL,`groupId` varchar(255) COLLATE utf8_general_ci NOT NULL,`userId` varchar(255) COLLATE utf8_general_ci NOT NULL, PRIMARY KEY (`Id`)) ENGINE=MyISAM;")[m
[32m+[m
[32m+[m[32m    def get_user_db(self, id, req_url):[m
[32m+[m
[32m+[m[32m        try:[m
[32m+[m[32m            mycursor.execute("SELECT * FROM `Users` WHERE id='{}'".format(id))[m
[32m+[m[32m        except mysql.connector.Error as err:[m
[32m+[m[32m            status_code = 400[m
[32m+[m[32m            error_message = "{}".format(err)[m
[32m+[m[32m            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)[m
[32m+[m[32m            return scim_error[m[41m [m
[32m+[m[32m        myresult = mycursor.fetchall()[m
[32m+[m[32m        if myresult:[m
[32m+[m[32m            row = [list(i) for i in myresult][0][m
[32m+[m[32m            userId = row[0][m
[32m+[m[32m            groups = self.get_groups_for_user(userId, req_url)[m
[32m+[m[32m            row.append(groups)[m
[32m+[m[32m            return scim_core.ParseSCIMUser(row, req_url)[m[41m            [m
[32m+[m[32m        else:[m
[32m+[m[32m            status_code = 404[m
[32m+[m[32m            error_message = "Not found."[m
[32m+[m[32m            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)[m
[32m+[m[32m            return scim_error[m
[32m+[m
[32m+[m[32m    def get_all_users_db(self, req_url, start_index, count):[m
[32m+[m
[32m+[m[32m        start_index = int(start_index)[m
[32m+[m[32m        count = int(count)[m
[32m+[m
[32m+[m[32m        try:[m
[32m+[m[32m            mycursor.execute("SELECT * FROM `Users` LIMIT {}, {}".format((start_index-1), count))[m
[32m+[m[32m        except mysql.connector.Error as err:[m
[32m+[m[32m            status_code = 400[m
[32m+[m[32m            error_message = "{}".format(err)[m
[32m+[m[32m            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)[m
[32m+[m[32m            return scim_error[m
[32m+[m[32m        myresults = mycursor.fetchall()[m
[32m+[m[32m        rows = [list(i) for i in myresults][m
[32m+[m[32m        for row in rows:[m
[32m+[m[32m            userId = row[0][m
[32m+[m[32m            groups = self.get_groups_for_user(userId, req_url)[m
[32m+[m[32m            row.append(groups)[m[41m     [m
[32m+[m[32m        total_results = 0[m
[32m+[m[32m        try:[m
[32m+[m[32m            mycursor.execute("SELECT * from `Users`")[m
[32m+[m[32m        except mysql.connector.Error as err:[m
[32m+[m[32m            status_code = 400[m
[32m+[m[32m            error_message = "{}".format(err)[m
[32m+[m[32m            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)[m
[32m+[m[32m            return scim_error[m
[32m+[m[32m        myresults = mycursor.fetchall()[m
[32m+[m[32m        for row in myresults:[m
[32m+[m[32m            total_results += 1[m
[32m+[m[32m        return scim_core.CreateSCIMUserList(start_index, count, total_results, req_url, rows)[m
[32m+[m[41m    [m
[32m+[m[32m    def get_filtered_users_db(self, req_url, attribute_name, attribute_value, start_index, count):[m
[32m+[m
[32m+[m[32m        start_index = int(start_index)[m
[32m+[m[32m        count = int(count)[m
[32m+[m[32m        try:[m
[32m+[m[32m            mycursor.execute("SELECT * FROM `Users` WHERE {} = '{}' LIMIT {}, {}".format(attribute_name, attribute_value, (start_index-1), count))[m
[32m+[m[32m        except mysql.connector.Error as err:[m
[32m+[m[32m            status_code = 400[m
[32m+[m[32m            error_message = "{}".format(err)[m
[32m+[m[32m            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)[m
[32m+[m[32m            return scim_error[m
[32m+[m[32m        myresults = mycursor.fetchall()[m
[32m+[m[32m        rows = [list(i) for i in myresults][m
[32m+[m[32m        for row in rows:[m
[32m+[m[32m            userId = row[0][m
[32m+[m[32m            groups = self.get_groups_for_user(userId, req_url)[m
[32m+[m[32m            row.append(groups)[m
[32m+[m[32m        total_results = 0[m
[32m+[m[32m        try:[m
[32m+[m[32m            mycursor.execute("SELECT * from `Users`")[m
[32m+[m[32m        except mysql.connector.Error as err:[m
[32m+[m[32m            status_code = 400[m
[32m+[m[32m            error_message = "{}".format(err)[m
[32m+[m[32m            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)[m
[32m+[m[32m            return scim_error[m
[32m+[m[32m        myresults = mycursor.fetchall()[m
[32m+[m[32m        for row in myresults:[m
[32m+[m[32m            total_results += 1[m
[32m+[m[32m        return scim_core.CreateSCIMUserList(start_index, count, total_results, req_url, rows)[m
[32m+[m[41m    [m
[32m+[m[32m    def get_groups_for_user(self, id, req_url):[m
[32m+[m[32m        try:[m
[32m+[m[32m            mycursor.execute("SELECT * from `GroupMemberships` WHERE userId = '{}'".format(id))[m
[32m+[m[32m        except mysql.connector.Error as err:[m
[32m+[m[32m            status_code = 400[m
[32m+[m[32m            error_message = "{}".format(err)[m
[32m+[m[32m            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)[m
[32m+[m[32m            return scim_error[m
[32m+[m[32m        myresults = mycursor.fetchall()[m
[32m+[m[32m        groups_for_user = [][m
[32m+[m[32m        if myresults:[m
[32m+[m[32m            rows = [list(i) for i in myresults][m
[32m+[m[32m            for group in rows:[m
[32m+[m[32m                groups_dict = {[m
[32m+[m[32m                    "value":"",[m
[32m+[m[32m                    "ref":"",[m
[32m+[m[32m                    "display":""[m
[32m+[m[32m                }[m[41m                [m
[32m+[m[32m                groupId = group[1][m
[32m+[m[32m                groups_dict["value"] = groupId[m
[32m+[m[32m                mycursor.execute("SELECT * FROM `Groups` WHERE id='{}'".format(groupId))[m
[32m+[m[32m                get_groupName = mycursor.fetchall()[m
[32m+[m[32m                if get_groupName:[m
[32m+[m[32m                    groupName = [list(i) for i in get_groupName][0][1][m
[32m+[m[32m                    groups_dict["display"] = groupName[m
[32m+[m[32m                    a = len(req_url)[m
[32m+[m[32m                    b = len('/Users/'+id)[m
[32m+[m[32m                    e = len('/Users')[m
[32m+[m[32m                    #c = len(req_url+"/"+id)[m
[32m+[m[32m                    if id in req_url:[m
[32m+[m[32m                        c = (a - b)[m
[32m+[m[32m                        d = req_url[0:c][m
[32m+[m[32m                        location = d + "/Groups/" + groupId[m
[32m+[m[32m                    else:[m
[32m+[m[32m                        c = (a - e)[m
[32m+[m[32m                        d = req_url[0:c][m
[32m+[m[32m                        location = d + "/Groups/" + groupId[m
[32m+[m[32m                    groups_dict["ref"] = location[m[41m                   [m
[32m+[m[32m                    groups_for_user.append(groups_dict)[m
[32m+[m[32m            return groups_for_user[m[41m                           [m
[32m+[m
[32m+[m[32m    def create_user_db(self, user_model, req_url):[m
[32m+[m[41m        [m
[32m+[m[32m        try:[m
[32m+[m[32m            mycursor.execute("SELECT * FROM `Users` WHERE userName='{}'".format(user_model['userName']))[m
[32m+[m[32m        except mysql.connector.Error as err:[m
[32m+[m[32m            status_code = 400[m
[32m+[m[32m            error_message = "{}".format(err)[m
[32m+[m[32m            scim_error = scim_core.CreateSCIMEerror(error_message, status_code)[m
[32m+[m[32m            return scim_error[m
[32m+[m[41m        [m
[32m+[m[32m        myresult = mycursor.fetchall()[m
[32m+[m
[32m+[m[32m        if myresult == []:[m
[32m+[m[32m            uid = str(uuid.uuid4())[m
[32m+[m[32m            req_url = req_url+'/'+uid[m
[32m+[m[32m            sql = "INSERT INTO `Users` (id, active, userName, givenName, middleName, familyName, email) VALUES (%s, %s, %s, %s, %s, %s, %s)"[m
[32m+[m[32m            val = (uid, user_model['active'], user_model['userName'], user_model['givenName'], user_model['middleName'], user_model['familyName'], user_model['email'])[m
[32m+[m[32m            try:[m[41m [m
[32m+[m[32m                mycursor.execute(sql, val)[m
[32m+[m[32m            except mysql.connector.Error as err:[m
[32m+[m[32m                status_code = 400[m
[32m+[m[32m                error_message = "{}".format(err)[m
[32m+[m[32m                scim_error = scim_core.CreateSCIMEerror(error_message, status_code)[m
[32m+[m[32m                return scim_error[m
[32m+[m[32m            #scim_core.CreateSCIMUser(uid, True, user_model['userName'], user_model['givenName'], user_model['familyName'], user_model['email'], req_url, user_model['middleName'], user_model['groups'])[m
[32m+[m[32m            if user_model["groups"] != []:[m
[32m+[m[32m                for group in user_model["groups"]:[m
[32m+[m[32m                    groupId = group["value"][m
[32m+[m[32m                    self.patch_group_db_add(uid, groupId)[m
[32m+[m[32m                return self.get_user_db(uid, req_url)[m
[32m+[m[32m            else:[m
[32m+[m[32m                return self.get_user_db(uid, req_url)[m
[32m+[m[32m        else:[m[41m [m
[32m+[m[32m            for row in myresult:[m
[32m+[m[32m                row = [list(i) for i in myresult][m
[32m+[m[32m                row = row[0][m
[32m+[m[32m                row = row[2][m
[32m+[m[32m            if row == user_model['userName']:[m
[32m+[m[32m                status_code = 409[m
[32m+[m[32m                error_message = "Conflict! User already exists"[m
[32m+[m[32m                scim_error = scim_core.CreateSCIMEerror(error_message, status_code)[m
[32m+[m[32m                return scim_error[m
[32m+[m
[32m+[m[32m    def update_user_db(self, user_model, id, req_url):[m
[32m+[m[41m        [m
[32m+[m[32m        try:[m
[32m+[m[32m            mycursor.execute("SELECT * FROM