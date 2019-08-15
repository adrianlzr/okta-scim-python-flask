def return_sp_config(url):
  data = {
    "schemas":
      ["urn:ietf:params:scim:schemas:core:2.0:ServiceProviderConfig"],
    "documentationUri": "http://example.com/help/scim.html",
    "patch": {
      "supported":True
    },
    "bulk": {
      "supported":False,
    },
    "filter": {
      "supported":True,
      "maxResults": 200
    },
    "changePassword": {
      "supported":False
    },
    "sort": {
      "supported":True
    },
    "etag": {
      "supported":False
    },
    "authenticationSchemes": [
      {
        "name": "OAuth Bearer Token",
        "description":
          "Authentication scheme using the OAuth Bearer Token Standard",
        "specUri": "http://www.rfc-editor.org/info/rfc6750",
        "documentationUri": "http://example.com/help/oauth.html",
        "type": "oauthbearertoken",
        "primary": True
      },
      {
        "name": "HTTP Basic",
        "description":
          "Authentication scheme using the HTTP Basic Standard",
        "specUri": "http://www.rfc-editor.org/info/rfc2617",
        "documentationUri": "http://example.com/help/httpBasic.html",
        "type": "httpbasic"
       }
    ],
    "meta": {
      "location": f"{url}",
      "resourceType": "ServiceProviderConfig",
      "created": "2019-08-08T04:56:22Z",
      "lastModified": "2019-08-08T05:56:22Z",
      "version": "W\/\"3694e05e9dff594\""
    }
  }
  return data


