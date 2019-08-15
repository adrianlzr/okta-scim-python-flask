import json, time, urllib.parse
from flask import Flask, request, Response, render_template
from core.cors import crossdomain
from core.Database import Database
from core.RequireAuth import auth_required
from operations.Users import Users
from operations. Groups import Groups
from core.ServiceProviderConfig import return_sp_config
ops_users = Users()
ops_groups = Groups()

app = Flask(__name__)

@app.route("/scim/v2/ServiceProviderConfig", methods =['GET'])
@crossdomain(origin='*')
def service_provider_config_route():
    url = request.base_url
    data = return_sp_config(url)
    response = app.response_class(
        response = json.dumps(data),
        status = 200,
        mimetype = 'application/json'
    )
    return response

@app.route("/scim/users")
@crossdomain(origin='*')
def users():
    req_url = request.base_url
    usr = ops_users.get_all_users(req_url, 1, 100)
    usr_all= usr["Resources"]
    i = 0
    all_users = []
    profileUrls = []
    while i < len(usr_all):
        userName = usr_all[i]["userName"]
        profileUrl = usr_all[i]["profileUrl"]
        all_users.append(userName)
        profileUrls.append(profileUrl)
        i += 1
    zip_users = zip(all_users, profileUrls)
    users = dict(zip_users)
    return render_template("index.html",users=users, title="All Users")
@app.route("/scim/users/<string:userId>")
@crossdomain(origin='*')
def user(userId):
    req_url = request.base_url
    usr = ops_users.get_user(userId, req_url)
    userName = usr["userName"]
    firstName = usr["name"]["givenName"]
    return render_template("profile.html",userName=userName, firstName=firstName, title=firstName)

@app.route("/scim/v2", methods = ['GET', 'OPTIONS'])
@crossdomain(origin='*')
@auth_required(method='oauth2')
def default_scim_route():
    response = app.response_class(
    response = "<h1>Hello World</h1>",
    status = 200,
    mimetype='text/html'   
    )
    return response

@app.route("/scim/v2/Users", methods = ['GET', 'POST', 'OPTIONS'])
@crossdomain(origin='*')
@auth_required(method='oauth2')
def users_route():
    req_url = request.base_url
    
    if request.method == 'GET':
        filters = ["userName", "givenName", "middleName", "familyName", "email"]
        start_index = request.args.get("startIndex")
        count =  request.args.get("count")
        if not start_index:
            start_index = 1
        if not count:
            count = 100
        
        f = request.args.get("filter")
        if f:
            f = urllib.parse.unquote(f)
            i = 0 
            while i < len(f):
                if filters[i] in f:
                    attribute_name = filters[i]
                    break
                i += 1
            #f - filter found in URL,  a - attributeName, e - end[index position] of string attributeName, t - total length of the filter string. 
            a = attribute_name 
            e = len(a)
            t = len(f)
            attribute_value = f[e:t].replace(' eq ', "").replace('"', "")
            filtered_users = ops_users.get_filtered_users(req_url, attribute_name, attribute_value, start_index, count)
            try:
                if filtered_users['status']:
                    http_code = filtered_users['status']
            except KeyError:
                    http_code = 200
                    pass             
            response = app.response_class(
                response = json.dumps(filtered_users),
                status = http_code,
                mimetype='application/scim+json'
            )
            return response            

        else: 
            all_groups = ops_users.get_all_users(req_url, start_index, count)
            try:
                if all_groups['status']:
                    http_code = all_groups['status']
            except KeyError:
                http_code = 200
                pass                
            response = app.response_class(
                response = json.dumps(all_groups),
                status = http_code,
                mimetype='application/scim+json'
            )
            return response 
        
    elif request.method == 'POST':
        data = request.data
        user_data_json = json.loads(data)
        new_user = ops_users.create_user(user_data_json, req_url)
        try:
            if new_user['status']:
                http_code = new_user['status']
        except KeyError:
            http_code = 201    
        response = app.response_class(
            response = json.dumps(new_user),
            status = http_code,
            mimetype='application/scim+json'
        )
        return response

@app.route("/scim/v2/Users/<string:id>", methods = ['GET', 'PUT', 'PATCH'])
@crossdomain(origin='*')
@auth_required(method='oauth2')
def users_by_id_route(id):
    id = str(id)
    req_url = request.base_url

    if request.method == 'GET':
        get_user = ops_users.get_user(id, req_url)

        try:
            if get_user['status']:
                http_code = get_user['status']
        except KeyError:
                http_code = 200
                pass         
        response = app.response_class(
            response = json.dumps(get_user),
            status = http_code,
            mimetype='application/scim+json'
        )    
        return response 

    elif request.method == 'PUT':
        data = request.data
        user_data_json = json.loads(data)
        update_user = ops_users.update_user(user_data_json, id, req_url)
        try:
            if update_user['status']:
                http_code = update_user['status']
        except KeyError:
            http_code = 200    
        response = app.response_class(
            response = json.dumps(update_user),
            status = http_code,
            mimetype='application/scim+json'
        )
        return response

    elif request.method == 'PATCH':
        data = request.data 
        user_data_json = json.loads(data)
        patch_user = ops_users.patch_user(user_data_json, id, req_url)
        try:
            if patch_user['status']:
                http_code = patch_user['status']
        except KeyError:
            http_code = 202  
        response = app.response_class( 
            response = json.dumps(patch_user),
            status = http_code,
            mimetype = 'application/scim+json'
        )
        return response

@app.route("/scim/v2/Groups", methods = ['GET', 'POST', 'OPTIONS'])
@crossdomain(origin='*')
@auth_required(method='oauth2')
def groups_route():    
    req_url = request.base_url

    if request.method == "GET" :
        start_index = request.args.get("startIndex")
        count =  request.args.get("count")
        filters = ["displayName"]

        if not start_index:
            start_index = 1
        if not count:
            count = 100
        
        f = request.args.get("filter")
        if f:
            f = urllib.parse.unquote(f)
            i = 0 
            while i < len(f):
                if filters[i] in f:
                    attribute_name = filters[i]
                    break
                i += 1
            #f - filter found in URL,  a - attributeName, e - end[index position] of string attributeName, t - total length of the filter string. 
            a = attribute_name 
            e = len(a)
            t = len(f)
            attribute_value = f[e:t].replace(' eq ', "").replace('"', "")
            filtered_groups = ops_groups.get_filtered_groups(attribute_name, attribute_value, req_url, start_index, count)
            try:
                if filtered_groups['status']:
                    http_code = filtered_groups['status']
            except KeyError:
                    http_code = 200
                    pass             
            response = app.response_class(
                response = json.dumps(filtered_groups),
                status = http_code,
                mimetype='application/scim+json'
            )
            return response
        else:
            all_groups = ops_groups.get_all_groups(req_url, start_index, count)
            try:
                if all_groups['status']:
                    http_code = all_groups['status']
            except KeyError:
                http_code = 200
                pass                
            response = app.response_class(
                response = json.dumps(all_groups),
                status = http_code,
                mimetype='application/scim+json'
            )
            return response

    elif request.method == 'POST':
        data = request.data
        group_data_json = json.loads(data)
        new_group = ops_groups.create_group(group_data_json, req_url)
        try:
            if new_group['status']:
                http_code = new_group['status']
        except KeyError:
            http_code = 201    
        response = app.response_class(
            response = json.dumps(new_group),
            status = http_code,
            mimetype='application/scim+json'
        )
        return response

@app.route("/scim/v2/Groups/<string:id>", methods = ['GET', 'PUT', 'PATCH', 'DELETE'])
@crossdomain(origin='*')
@auth_required(method='oauth2')
def groups_by_id_route(id):
    id = str(id)
    req_url = request.base_url

    if request.method == "GET":
        get_group = ops_groups.get_group(id, req_url)

        try:
            if get_group['status']:
                http_code = get_group['status']
        except KeyError:
                http_code = 200
                pass         
        response = app.response_class(
            response = json.dumps(get_group),
            status = http_code,
            mimetype='application/scim+json'
        )
        return response

    if request.method == "PUT":
        response = app.response_class(
            response = "<h1>Hello World</h1>",
            status = 200,
            mimetype='text/html'   
            )
        return response
    
    if request.method == "PATCH":
        
        data = request.data
        group_data_json = json.loads(data)
        patch_group = ops_groups.patch_group(group_data_json, id, req_url)
        try:
            if patch_group["status"]:
                http_code = patch_group["status"]
        except KeyError:
            http_code = 202
        response = app.response_class(
            response = json.dumps(patch_group),
            status = http_code,
            mimetype = "application/scim+json"
        )
        return response

    if request.method == "DELETE":

        delete_group = ops_groups.delete_group(id, req_url)
        response = app.response_class(
            response = '',
            status = 204,
            mimetype = "application/scim+json"
        )
        return response        
    
if __name__ == '__main__':
    app.run(debug=True)