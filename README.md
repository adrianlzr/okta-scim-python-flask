# Python-Flask SCIM Server Example. 
Python SCIM Server (based on Flask) that supports /Users and /Groups endpoint, created as a POC for the Okta SCIM Server. Has successfully passed the [CRUD Okta Runscope test](https://www.okta.com/integrate/documentation/scim/#run-the-second-set-of-runscope-tests-okta-scim-11-crud-test-or-okta-scim-20-crud-test)
* Written based on [Dragos Gaftoneanu's PHP SCIM Server.](https://github.com/dragosgaftoneanu-okta/php-scim-server)

ℹ️ Disclaimer: This SCIM server was built in order to troubleshoot different SCIM use-cases and not to be used in production. The script is provided AS IS without warranty of any kind. Okta disclaims all implied warranties including, without limitation, any implied warranties of fitness for a particular purpose. We highly recommend testing scripts in a preview environment if possible.

* Please note that this example might suffer modifications at any giventime. It is currently a "work in progress". 

## Requirements.
* Python3.6 - minimum required version. 
* Pip
* Python Virtual Env - I recommend installing [virtualenv](https://www.geeksforgeeks.org/python-virtual-environment/)
* Ngrok 
* [Okta Developer Account](https://developer.okta.com/signup/)

-------------

## Getting started.

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

# Bugs?
If you find any bugs with this SCIM server please open a new Issue and it will be investigated. 

# Suggestions? 
Please feel free to contact me at adrian.lazar@okta.com. 
