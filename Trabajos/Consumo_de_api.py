import json
from urllib import response
import requests

dic_data = {'swtiches':[
    {"model":'CAT3750',
     "model":'CAT3760'}
]}

dic_data2={
    'server':[
    {"model":'7206VXR',
     "so" :'Cisco IOS',
     "vendor" :'Cisco',
     "type" :'hardware'
     }],
    'router1':[
    {'name':'servidor_1',
     'service':'WEB',
     'remote_conection':'SSH',
     'ip':'192.168.10.1'
                }],
    'router2':[
    {'name':'servidor_2',
     'service1':'DNS',
     'service2':'WEB',
     'ip':'192.168.10.2'
                }],
    'router3':[
    {'name':'servidor_3',
     'service1':'FTP',
     'service2':'DHCP',
     'ip':'192.168.10.3'
                }]
    }

print(json.dumps(dic_data, indent=2))
print(json.dumps(dic_data2, indent=3))

def form_json():
    dic_data = {
        'switches': [
            {'model': 'CAT3750'},
            {'model': 'CAT3760'}
        ],
        'routers': {
            'name': 'CSR100V',
            'vendedor': 'cisco',
            'type': 'hardware'
        }
    }

    print(json.dumps(dic_data, indent=4, sort_keys=True))
    with open("./data/infraestructure.json", 'w') as file:
        json.dump(dic_data, file, indent=4, sort_keys=True)

def get_api_ips():
    response = requests.get('http://ip-api.com/json/24.48.0.1')
    print(response.json())

def get_api_geolocation(ip):
    url = f'http://ip-api.com/json/8.8.8.8'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'success':
            print(json.dumps(data, indent=4, sort_keys=True))
        else:
            print(f"Error: {data['message']}")
    else:
        print(f"Failed to retrieve data: {response.status_code}")


url = "https://api.meraki.com/api/v1/organizations"

payload = None

headers = {
    "X-Cisco-Meraki-API-Key": "75dd5334bef4d2bc96f26138c163c0a3fa0b5ca6",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

response = requests.request('GET', url, headers=headers, data = payload)



if __name__ == "__main__":
    # form_json()
    get_api_ips()
    ip_address = '208.80.152.201'
    get_api_geolocation(ip_address)
    print(response)

