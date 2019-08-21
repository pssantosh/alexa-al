import json
import requests
from flask import Flask
app = Flask(__name__)

def get_AL_Profile_Token():
    api_basic_token = 'V0VCX0tFWV9STTpkZzlkeUZyOXZUcm0='
    api_url_base = 'https://d1vsen-pcapi.epsilonagilityloyalty.com/'
    token_Header = {
                'Program-Code': 'RMART', 
                'Accept-Language': 'en-US',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': 'Basic {0}'.format(api_basic_token)
                }
    data = {'grant_type':'password','username':'Williamson','password':'Kane.123','response_type':'token'}
    api_url = '{0}api/v1/authorization/profiles/tokens'.format(api_url_base)
    
    response = requests.post(api_url, headers=token_Header, data=data)
    
    if response.status_code == 201:
        res = response.json()
        api_token = res['AccessToken']
        return  [res['AccessToken'], res['ProfileId']]
    else:
        return None

def get_Profile_Details(tokenDetails):
    api_basic_token = 'V0VCX0tFWV9STTpkZzlkeUZyOXZUcm0='
    api_url_base = 'https://d1vsen-pcapi.epsilonagilityloyalty.com/'
    request_Header = {
                        'Program-Code': 'RMART',
                        'Accept-Language': 'en-US',
                        'Content-Type': 'application/json',
                        'Authorization': 'OAuth {0}'.format(tokenDetails[0])
                    }
    
    api_url = '{0}api/v1/profiles/{1}'.format(api_url_base, tokenDetails[1])
    response = requests.get(api_url, headers=request_Header)
    if response.status_code == 200:
        res = response.json()
        return  '{0} {1}'.format(res['FirstName'], res['LastName'])
    else:
        return ''

def get_Profile_Points(tokenDetails):
    api_basic_token = 'V0VCX0tFWV9STTpkZzlkeUZyOXZUcm0='
    api_url_base = 'https://d1vsen-pcapi.epsilonagilityloyalty.com/'
    request_Header = {
                        'Program-Code': 'RMART',
                        'Accept-Language': 'en-US',
                        'Content-Type': 'application/json',
                        'Authorization': 'OAuth {0}'.format(tokenDetails[0])
                    }
    
    api_url = '{0}api/v1/profiles/{1}/points/balance?status=A'.format(api_url_base, tokenDetails[1])
    response = requests.get(api_url, headers=request_Header)
    result = response.json()
    if response.status_code == 200:
        points = int(result['PointsBalance'][0]['PointAmount'])
        Pts = str(points)
        return Pts
    else:
        return None

@app.route("/")
def home():
    return 'Welcome Home!'

@app.route("/GetUser")
def GetUser():
    token_Details = get_AL_Profile_Token()
    username = get_Profile_Details(token_Details)
    return username

@app.route("/Points")
def GetPointBalance():
    token_Details = get_AL_Profile_Token()
    points = get_Profile_Points(token_Details)
    return points


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)