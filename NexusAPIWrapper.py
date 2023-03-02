from config import settings
import requests
from datetime import datetime, timedelta

class NexusAPI:
    def __init__(self):
        self.token_url = settings.api_url_token
        self.headers = {
            "Authorization": "Bearer {{access_token}}"
        }
        self.getTokens()

    def getTokens(self):
        self.api_credentials = {
            "grant_type": settings.grant_type,
            "client_id": settings.client_id,
            "client_secret": settings.client_secret
        }
        response = requests.post(self.token_url, data=self.api_credentials).json()
        
        self.access_token = response["access_token"]
        self.refresh_token = response["refresh_token"]
        self.headers["Authorization"] = "Bearer {}".format(self.access_token)

        self.setTokenExpiration(response["expires_in"], response["refresh_expires_in"])

    def setTokenExpiration(self, access_expiration, refresh_expiration):
        self.access_token_expires = datetime.now() + timedelta(seconds=(access_expiration-15))
        self.refresh_token_expires = datetime.now() + timedelta(seconds=(refresh_expiration-15))

    def checkToken(self):
        access_token_delta = (self.access_token_expires - datetime.now()).total_seconds()
        refresh_token_delta = (self.refresh_token_expires - datetime.now()).total_seconds()
        if access_token_delta < 0:
            if refresh_token_delta < 0:
                self.getTokens()
            else:
                self.getTokenFromRefresh()
    
    def getTokenFromRefresh(self):
        self.api_credentials = {
            "grant_type": settings.grant_type,
            "client_id": settings.client_id,
            "client_secret": settings.client_secret,
            "refresh_token": self.refresh_token
        }
        response = requests.post(self.token_url, data=self.api_credentials).json()
        self.access_token = response["access_token"]
        self.refresh_token = response["refresh_token"]
        self.headers["Authorization"] = "Bearer {}".format(self.access_token)
        self.setTokenExpiration(response["expires_in"], response["refresh_expires_in"])

    def getHomeRessource(self):
        self.checkToken()
        res = requests.get(settings.api_url_base, headers=self.headers)
        return res.json()
    
    def getOrganizationsTree(self):
        self.checkToken()
        url = settings.api_url_base + "organizations/tree"
        res = requests.get(url, headers=self.headers)
        return res.json()
    
    def findProfessionals(self, search_term):
        self.checkToken()
        url = settings.api_url_base + "professionals/?query={}".format(search_term)
        res = requests.get(url, headers=self.headers)
        return res.json()
    
    def getProfessionalPrototype(self):
        self.checkToken()
        url = settings.api_url_base + "professionals/prototype"
        res = requests.get(url, headers=self.headers)
        return res.json()
    
    def getProfessional(self, user_id):
        self.checkToken()
        url = settings.api_url_base + "professionals/{}".format(user_id)
        res = requests.get(url, headers=self.headers)
        return res.json()
    
    def getProfessionalPermissionAssignments(self, user_id):
        self.checkToken()
        url = settings.api_url_base + "professionals/{}/permissionAssignments".format(user_id)
        res = requests.get(url, headers=self.headers)
        return res.json()
    
    def getProfessionalPermissionsTree(self, user_id):
        self.checkToken()
        url = settings.api_url_base + "professionals/{}/permissions/tree".format(user_id)
        res = requests.get(url, headers=self.headers)
        return res.json()
    
    def getProfessionalRoles(self, user_id):
        self.checkToken()
        url = settings.api_url_base + "professionals/{}/availableRoles".format(user_id)
        res = requests.get(url, headers=self.headers)
        return res.json()
    
    def createProfessional(self, prototype_dict):
        self.checkToken()
        url = settings.api_url_base + "professionals"
        res = requests.post(url, headers=self.headers, json=prototype_dict)
        return res.json()
    
    def getProfessionalConfiguration(self, user_id):
        self.checkToken()
        url = settings.api_url_base + "professionals/configuration/{}".format(user_id)
        res = requests.get(url, headers=self.headers)
        return res.json()
