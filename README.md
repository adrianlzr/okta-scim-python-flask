-------------
# REPRO for case 00649440 JIRA - OKTA-244438
## DO NOT USE if you're not looking for reproducing the same behavior.
### Response times have been 'artifically increased' with time.sleep().  
-------------

# Python-Flask SCIM Server Example. 
Python SCIM Server (based on Flask) that supports /Users and /Groups endpoint, created as a POC for the Okta SCIM Server. Has successfully passed the [CRUD Okta Runscope test](https://www.okta.com/integrate/documentation/scim/#run-the-second-set-of-runscope-tests-okta-scim-11-crud-test-or-okta-scim-20-crud-test)
* Written based on [Dragos Gaftoneanu's PHP SCIM Server.](https://github.com/dragosgaftoneanu-okta/php-scim-server)

ℹ️ Disclaimer: This SCIM server was built in order to troubleshoot different SCIM use-cases and not to be used in production. The script is provided AS IS without warranty of any kind. Okta disclaims all implied warranties including, without limitation, any implied warranties of fitness for a particular purpose. We highly recommend testing scripts in a preview environment if possible.

* Please note that this example might suffer modifications at any giventime. It is currently a "work in progress". 

-------------

## Table of Contents:
* [Requirements](https://github.com/adrianlazar-personal/okta-scim-python-flask#requirements)
* [Endpoints](https://github.com/adrianlazar-personal/okta-scim-python-flask#Endpoints)
* [Getting Sarted](https://github.com/adrianlazar-personal/okta-scim-python-flask#getting-started)
    * [Local Environment Setup](https://github.com/adrianlazar-personal/okta-scim-python-flask#local-environment-setup)
    * [Okta Setup](https://github.com/adrianlazar-personal/okta-scim-python-flask#okta-setup)
* [OAuth Authentication](https://github.com/adrianlazar-personal/okta-scim-python-flask#oauth-authentication)
* [Bugs](https://github.com/adrianlazar-personal/okta-scim-python-flask#bugs)
* [Suggestions](https://github.com/adrianlazar-personal/okta-scim-python-flask#suggestions)

-------------

## Requirements.
* MYSQL Database (I am using XAMPP for local development)
* Python3.6 - minimum required version. 
* Pip
* Python Virtual Env - I recommend installing [virtualenv](https://www.geeksforgeeks.org/python-virtual-environment/)
* Ngrok 
* [Okta Developer Account](https://developer.okta.com/signup/)

-------------

## Endpoints.

#### Base Endpoints
* /scim/users - Returns all the users(no filtering), no auth enforced.
* /scim/v2 - Base SCIM path - auth enforced
* /scim/v2/ServiceProviderConfig - [RFC7644#section-4](https://tools.ietf.org/html/rfc7644#section-4)
* *Other SCIM-relevant endpoints will be added soon.*
#### Users Endpoints
* /scim/v2/Users - Base Users path: Supported HTTP methods: [**GET**, **POST**]
* /scim/v2/Users/**{userId}** - Individual User path: Supported HTTP methods: [**GET**, **POST**, **PUT**, **PATCH**]
#### Groups endpoints
* /scim/v2/Groups - Base Groups path: Supported HTTP methods: [**GET**, **POST**]
* /scim/v2/Groups/**{groupId}** - Individual Group path: Supported HTTP methods: [**GET**, **POST**, **PATCH**, **DELETE**] - *PUT will be supported soon.*

-------------

## Getting started.
### Local Environment Setup
**This example assumes you are using a Windows machine. If you are using a different OS, change the path mindset accordingly.**

The project base path will be: 
```
C:\Users\your_user\Desktop
```

Let's create a new folder called "scim-server", which will server as the root of our project and clone this example.
```
mkdir scim-server && cd scim-server
git clone https://github.com/adrianlazar-okta/flask-python-scim-server.git
```

Initialize a new virtual environment where all the dependencies will be installed
```
virtualenv "name"(ex scimvenv)
```
Start the environment
```
cd path/to/virtualenv(ex cd C:\Users\your_user\Desktop\scim-server\scimvenv\Scripts)
activate
cd C:\Users\your_user\Desktop\scim-server
```
Install the dependencies 
```
python -m pip install -r requirements.txt
```
Install [XAMPP](https://www.apachefriends.org/download.html) and start the the mysql server and create a database named 'scim'
```
CREATE DATABASE scim;
```
Start the server

**Windows Users:**
```
python run.py
```
**Other OS:**
```
python3 run.py
```
* Please note that sometimes pip will not install all the dependecies successfully. Keeping an eye on the errors prompted when the server might fail will be really helpful. 
Start ngrok to listen on port 5000 ( port used by the scim server). 
```
ngrok http 5000
```
Now you can access http://localhost:4040 to monitor the trafic to your scim server running on port **5000**. 

## Okta Setup
After you have created a free account on [Okta Developer Account](https://developer.okta.com/signup/), you should have access to your Okta Admin dashboard.

Let's create a new application by using the [Okta Application Integration Wizzard](https://help.okta.com/en/prod/Content/Topics/Apps/Apps_App_Integration_Wizard.htm):
- Okta Admin UI -> Applications -> Add Application -> Create New App -> Platform: Web, Sign on method - SAML 2.0 (I will build a SAML app with Flask later.)

- Follow the configuration prompts, provide the requested URLs (any url will work, for ex https://google.com).

- Once the application is created, go to the General Tab -> Edit -> Select the option "SCIM" on the Provisioning section and Save.

- The Provisioning Tab should now be available. On this Tab, let's edit the settings, provide the SCIM connector base URL (if you are using ngrok, provide the url from ngrok so you can intercept the http requests, and append /scim/v2 at the end.)

- Unique identifier field for users: **userName**

- Select all the **Supported provisioning actions**

- Authentication mode: This SCIM Server Supports **Basic Auth** and **Oauth2**. 

- For Basic Auth, the credentials are: userName: **user** and password: **p@ss** (these values can be modified in [core->RequireAuth.py](https://github.com/adrianlazar-personal/okta-scim-python-flask/blob/f51edff3388ec0d9c5e7c72d5937f9d9ca0a116b/core/RequireAuth.py#L47))

- If you would like to use OAuth2, see the [OAuth Authentication](https://github.com/adrianlazar-personal/okta-scim-python-flask#oauth-authentication) section.

- Test Connector Configuration

-------------

## OAuth Authentication

#### ℹ️ Disclaimer: 
* Okta Only supports the [Authorization Code Flow](https://developer.okta.com/docs/guides/implement-auth-code/overview/) for SCIM integrations.
* At the time being, the SCIM Server [RequireAuth module](https://github.com/adrianlazar-personal/okta-scim-python-flask/blob/master/core/RequireAuth.py) can only verify the Token  Validity Remotely. This module allows you to disable Okta as the default Authorization Provider: *@auth_required(method="oauth2", **okta=False**)*. The second paramter"okta" is not a required parameter, and it's default value is set to **True**. 

*Furthermore, currently there is no actual validation. This is a work in progress. I will create a method for validating any type of JWT locally.* 

#### Leveraging Okta as the Authorization Server:
* Create a OIDC Web App - Okta Admin UI -> Applications -> Add Aplication -> Create New App -> Platform: Web,  Sign on method: OpenID Connect
* Login Redirect URL: This will be composed from: 
    * Production domain: https://system-admin.okta.com/admin/app/cpc/{application_name}/oauth/callback
    * Preview domain: https://system-admin.oktapreview.com/admin/app/cpc/{application_name}/oauth/callback
    * **{application_name}** is the internal SCIM application name created above. This can be found in Okta Admin ->
        Directories -> Profile Editor -> SCIM app - Profile -> Variable name
* Assign yourself (Super Admin User) to the OIDC application you just created
* Before moving on to the final step, in order for this flow to succeed, you need to configure a default scope for your Authorization Server. 
    * Custom Authorization Server is required!!
    * Okta Admin UI -> Security -> API -> Authorization Servers -> Select the "default" server -> Scopes -> Add Scope
        -> Name: authorization_service, Display Name: SCIM Authorization Service, Check the option "Set as a default scope."
    * *A default scope is required because this process does not allow you to specify a scope to be used. Using Okta as the Authorization server (URL PATH /oauth2/v1/xxx) will not allow you to set a default scope and the request will fail.*
* SCIM Application -> On the Provisioning tab (Integration), on the Authentication mode, select Oauth 2
* After Oauth 2 is selected 4 new fileds will need to be configured:
    * Access token endpoint URI: https://yourOktaDomain.okta/oktapreview.com/oauth2/v1/{authorizationServerId}/token
    * Authorization endpoint URI: https://yourOktaDomain.okta/oktapreview.com/oauth2/v1/{authorizationServerId}/authorize
    * Client ID: The client_id of the OIDC app created above
    * Client SECRET: The client_secret of the OIDC app created above
* Save and Authenticate with the App to generate the Access Token

#### Leveraging A different Oauth2 Provider as the Authorization Server:

* SCIM Application -> On the Provisioning tab (Integration), on the Authentication mode, select Oauth 2
* After Oauth 2 is selected 4 new fileds will need to be configured:
    * Access token endpoint URI: https://your.oauth2.provider/token
    * Authorization endpoint URI: https://your.oauth2.provider/authorize
    * Client ID: The client_id generated by your oauth2 provider
    * Client SECRET: The client_secret generated by your oauth2 provider
* Save and Authenticate with the App to generate the Access Token

# To Be Continued 
* Upcoming: Documentation will be updated to include Example SCIM Operations that are supported by this server.

# Bugs?
If you find any bugs with this SCIM server please open a new Issue and it will be investigated. 

# Suggestions? 
Please feel free to contact me at adrian.lazar@okta.com. 
