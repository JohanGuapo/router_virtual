import json
import requests
requests.packages.urllib3.disable_warnings()
from flask import Flask, render_template

def get_interfaces():
    module="data/ietf-interfaces:interfaces"
    resp = requests.get(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)
    print(json.dumps(resp.json(), indent=4))
    data_json = resp.json()

    for key, valor in data_json.items():
        print(f'Nombre de la interface: {valor["interface"][0]['name']}')
        print(f'Descripción de la interface: {valor["interface"][0]['description']}')
        print(f'Status de la interface: {valor["interface"][0]['enabled']}')
        
    else:
        print(f'Error al realizar la consulta del modulo {module}')
        
        
def get_resconf_native():
    module = "data/Cisco-IOS-XE-native:native"
    resp = requests.get(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 200:
        print(json.dumps(resp.json(), indent=4))
    else:
        print(f'Error al realizar la consulta del modulo {module}')
        
def get_banner():
    module = "data/Cisco-IOS-XE-native:native/banner/motd"
    resp = requests.get(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 200:
        print(json.dumps(resp.json(), indent=4))
    else:
        print(f'Error al realizar la consulta del modulo {module}')
        
def put_banner():
    banner = {
        "Cisco-IOS-XE-native:motd": {
            "banner": "#error no puedes entrar#"
        }
    }
    module = "data/Cisco-IOS-XE-native:native/banner/motd"
    resp = requests.put(f'{api_url}{module}',data=json.dumps(banner), auth=basicauth, headers=headers, verify=False)
    print(resp.status_code)
    
    print(banner)
     
def get_ip_domain():
    module = "data/Cisco-IOS-XE-native:native/ip/domain"
    resp = requests.get(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)
    
    if resp.status_code == 200:
        data_json = resp.json()
        print(json.dumps(data_json, indent=4))
        
        try:
            domain_name = data_json["Cisco-IOS-XE-native:domain"]["name"]
            print(f'Nombre de dominio: {domain_name}')
        except KeyError:
            print('Error: No se pudo encontrar el nombre de dominio en la respuesta.')
    else:
        print(f'Error al realizar la consulta del módulo {module}. Status code: {resp.status_code}')

def delete_ip_domain():
    module = "data/Cisco-IOS-XE-native:native/ip/domain"
    resp = requests.delete(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)
    
    if resp.status_code == 204:
        print('El nombre de dominio ha sido eliminado exitosamente.')
    else:
        print(f'Error al realizar la eliminación del módulo {module}. Status code: {resp.status_code}')
    
def delete_ip_domain():
    module = "data/Cisco-IOS-XE-native:native/ip/domain"
    resp = requests.delete(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)
    
    if resp.status_code == 204:
        print('El nombre de dominio ha sido eliminado exitosamente.')
    else:
        print(f'Error al realizar la eliminación del módulo {module}. Status code: {resp.status_code}')


def post_hostname(new_hostname):
    hostname_data = {
        "Cisco-IOS-XE-native:hostname": new_hostname
    }
    module = "data/Cisco-IOS-XE-native:native/hostname"
    resp = requests.put(f'{api_url}{module}', data=json.dumps(hostname_data), auth=basicauth, headers=headers, verify=False)
    
    if resp.status_code == 204:
        print(f'Se ha cambiado el nombre de host a "{new_hostname}" exitosamente.')
    else:
        print(f'Error al cambiar el nombre de host a "{new_hostname}". Status code: {resp.status_code}')
        
          
    
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('/index.html')



if __name__ == '__main__':
    app.run(debug=True)

    api_url = "https://192.168.56.101/restconf/"
    headers = {"Accept": "application/yang-data+json",
               "Content-type": "application/yang-data+json"
               }
    basicauth = ("cisco", "cisco123!")
    
    domain_name = "example.netacad.com"  # Reemplaza con el dominio que deseas agregar
    new_hostname = "RT-01"
    
    #get_interfaces()
    #get_resconf_native()
    #get_banner()
    #put_banner()
    get_ip_domain
    delete_ip_domain
    