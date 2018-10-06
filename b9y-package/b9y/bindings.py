#!/usr/bin/env python
import requests, json

default_user = "admin"
default_password = "changeme"
default_host="http://localhost:8080"

class B9y:

    def __init__(self, endpoint = default_host, username = default_user, password = default_password):
        self.endpoint = endpoint
        self.username = username
        self.password = password

        url = self.endpoint + "/auth/token?raw"
        payload = {'username': self.username, 'password': self.password}
        headers = {'Content-Type': "application/json"}

        try:
            response = requests.request("POST", url, json=payload, headers=headers)
        except:
            print("ERROR: Cannot connect to " + self.endpoint)
            exit(1)
        if response.status_code == 200:
            self.token = response.text
            return(None)
        else:
            print("ERROR: Unable to login with these connection details.")
            exit(1)

    def info(self):
        url = self.endpoint + "/"
        response = requests.request("GET", url)
        if response.status_code == 200:
            res = json.loads(response.text)
            return res["instance"], res["release"]

    def get(self, key):
        url = self.endpoint + "/keys/" + str(key)
        headers = {'Authorization': "Bearer:" + self.token}
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            return(response.text)
        else:
            return(None)

    def incr(self, key):
        url = self.endpoint + "/incr/" + str(key)
        headers = {'Authorization': "Bearer:" + self.token}
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            return(response.text)
        else:
            return(None)

    def set(self, key, value):
        url = self.endpoint + "/keys/" + key
        headers = {'Authorization': "Bearer:" + self.token}
        payload = value
        response = requests.request("PUT", url, data=payload, headers=headers)

        if response.status_code == 200:
            return(True)
        else:
            raise ValueError("ERROR: key invalid or quota exceeded (" + str(response.status_code) + ")")

    def push(self, key, value):
        url = self.endpoint + "/lists/" + key
        headers = {'Authorization': "Bearer:" + self.token}
        payload = value
        response = requests.request("POST", url, data=payload, headers=headers)

        if response.status_code == 200:
            return(True)
        else:
            raise ValueError("ERROR: key invalid or quota exceeded (" + str(response.status_code) + ")")

    def pop(self, key):
        url = self.endpoint + "/lists/" + key
        headers = {'Authorization': "Bearer:" + self.token}
        response = requests.request("GET", url, headers=headers)

        if response.status_code == 200:
            return(response.text)
        else:
            return(None)
