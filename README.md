# Python-Flask SCIM Server Example. 
Python SCIM Server (based on Flask) that supports /Users and /Groups endpoint, created as a POC for the Okta SCIM Server. Has successfully passed the [CRUD Okta Runscope test](https://www.okta.com/integrate/documentation/scim/#run-the-second-set-of-runscope-tests-okta-scim-11-crud-test-or-okta-scim-20-crud-test)
* Written based on [Dragos Gaftoneanu's PHP SCIM Server.](https://github.com/dragosgaftoneanu-okta/php-scim-server)

ℹ️ Disclaimer: This SCIM server was built in order to troubleshoot different SCIM use-cases and not to be used in production. The script is provided AS IS without warranty of any kind. Okta disclaims all implied warranties including, without limitation, any implied warranties of fitness for a particular purpose. We highly recommend testing scripts in a preview environment if possible.

* Please note that this example might suffer modifications at any giventime. It is currently a "work in progress". 

## Requirements.
* MYSQL Database (I am using XAMPP for local development)
* Python3.6 - minimum required version. 
* Pip
* Python Virtual Env - I recommend installing [virtualenv](https://www.geeksforgeeks.org/python-virtual-environment/)
* Ngrok 
* [Okta Developer Account](https://developer.okta.com/signup/)

-------------

## Getting started.
### Local environment setup
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
python3 -m pip install -r requirements.txt
```
Start the mysql server and create a database named 'scim'
```
CREATE DATABASE scim;
```
Start the server
```
python3 scim.py
```
* Please note that sometimes pip will not install all the dependecies successfully. Keeping an eye on the errors prompted when the server might fail will be really helpful. 
Start ngrok to listen on port 5000 ( port used by the scim server). 
```
ngrok http 5000
```
Now you can access http://localhost:4040 to monitor the trafic to your scim server running on port 5000. 

## Okta Setup
After you have created a free account on [Okta Developer Account](https://developer.okta.com/signup/), you should have access to your Okta Admin dashboard. 
Let's create a new application by using the Okta Application Integration Wizzard:
- Okta Admin UI -> Applications -> Add Application -> Create New App -> Platform: Web, Sign on method - SAML 2.0 (I will build a SAML app with Flask later.)
- Follow the configuration prompts, provide the requested URLs (any url will work, for ex https://google.com).
- Once the application is created, go to the General Tab -> Edit -> Select the option "SCIM" on the Provisioning section and Save.
- The Provisioning Tab should now be available. On this Tab, let's edit the settings, provide the SCIM connector base URL (if you are using ngrok, provide the url from ngrok so you can intercept the http requests, and append /scim/v2 at the end.)
- Unique identifier field for users: *userName*
- Authentication mode: This SCIM Server Supports Basic Auth and Oauth2. 
- For Basic Auth, the credentials are: userName: 'user' and password: 'p@ss' (these values can be modified in [core->RequireAuth.py](https://github.com/adrianlazar-personal/okta-scim-python-flask/blob/f51edff3388ec0d9c5e7c72d5937f9d9ca0a116b/core/RequireAuth.py#L47))
- If you would like to use Oauth2, see the bellow section.
# Bugs?
If you find any bugs with this SCIM server please open a new Issue and it will be investigated. 

# Suggestions? 
Please feel free to contact me at adrian.lazar@okta.com. 
