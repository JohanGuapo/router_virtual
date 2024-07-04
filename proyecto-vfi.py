import json
import requests
requests.packages.urllib3.disable_warnings()
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

api_url = "https://192.168.56.101/restconf/"
headers = {
    "Accept": "application/yang-data+json",
    "Content-type": "application/yang-data+json"
}
basicauth = ("cisco", "cisco123!")

def get_interfaces():
    module = "data/ietf-interfaces:interfaces"
    resp = requests.get(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 200:
        return resp.json()
    else:
        return {'error': f'Error al realizar la consulta del módulo {module}'}

def get_resconf_native():
    module = "data/Cisco-IOS-XE-native:native"
    resp = requests.get(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 200:
        return resp.json()
    else:
        return {'error': f'Error al realizar la consulta del módulo {module}'}

def get_banner():
    module = "data/Cisco-IOS-XE-native:native/banner/motd"
    resp = requests.get(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 200:
        return resp.json()
    else:
        return {'error': f'Error al realizar la consulta del módulo {module}'}

def put_banner(new_banner):
    banner = {
        "Cisco-IOS-XE-native:motd": {
            "banner": new_banner
        }
    }
    module = "data/Cisco-IOS-XE-native:native/banner/motd"
    resp = requests.put(f'{api_url}{module}', data=json.dumps(banner), auth=basicauth, headers=headers, verify=False)
    return {'status_code': resp.status_code, 'banner': banner}

def get_ip_domain():
    module = "data/Cisco-IOS-XE-native:native/ip/domain"
    resp = requests.get(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 200:
        data_json = resp.json()
        try:
            domain_name = data_json["Cisco-IOS-XE-native:domain"]["name"]
            return {'domain_name': domain_name}
        except KeyError:
            return {'error': 'No se pudo encontrar el nombre de dominio en la respuesta.'}
    else:
        return {'error': f'Error al realizar la consulta del módulo {module}. Status code: {resp.status_code}'}

def delete_ip_domain():
    module = "data/Cisco-IOS-XE-native:native/ip/domain"
    resp = requests.delete(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 204:
        return {'message': 'El nombre de dominio ha sido eliminado exitosamente.'}
    else:
        return {'error': f'Error al realizar la eliminación del módulo {module}. Status code: {resp.status_code}'}

def post_ip_domain(domain_name):
    domain_data = {
        "Cisco-IOS-XE-native:domain": {
            "name": domain_name
        }
    }
    module = "data/Cisco-IOS-XE-native:native/ip/domain"
    resp = requests.put(f'{api_url}{module}', data=json.dumps(domain_data), auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 204:
        return {'message': f'Se ha agregado el dominio "{domain_name}" exitosamente.'}
    else:
        return {'error': f'Error al agregar el dominio "{domain_name}". Status code: {resp.status_code}'}

def get_hostname():
    module = "data/Cisco-IOS-XE-native:native/hostname"
    resp = requests.get(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 200:
        data_json = resp.json()
        return data_json
    else:
        return {'error': f'Error al realizar la consulta del módulo {module}. Status code: {resp.status_code}'}

def post_hostname(new_hostname):
    hostname_data = {
        "Cisco-IOS-XE-native:hostname": new_hostname
    }
    module = "data/Cisco-IOS-XE-native:native/hostname"
    resp = requests.put(f'{api_url}{module}', data=json.dumps(hostname_data), auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 204:
        return {'message': f'Se ha cambiado el nombre de host a "{new_hostname}" exitosamente.'}
    else:
        return {'error': f'Error al cambiar el nombre de host a "{new_hostname}". Status code: {resp.status_code}'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/interfaces', methods=['GET'])
def interfaces():
    return jsonify(get_interfaces())

@app.route('/resconf-native', methods=['GET'])
def resconf_native():
    return jsonify(get_resconf_native())

@app.route('/banner', methods=['GET'])
def banner():
    return jsonify(get_banner())

@app.route('/banner', methods=['PUT'])
def update_banner():
    new_banner = request.json.get('new_banner')
    return jsonify(put_banner(new_banner))

@app.route('/ip-domain', methods=['GET'])
def ip_domain():
    return jsonify(get_ip_domain())

@app.route('/ip-domain', methods=['DELETE'])
def delete_domain():
    return jsonify(delete_ip_domain())

@app.route('/ip-domain', methods=['PUT'])
def add_domain():
    domain_name = request.json.get('domain_name')
    return jsonify(post_ip_domain(domain_name))

@app.route('/hostname', methods=['GET'])
def hostname():
    return jsonify(get_hostname())

@app.route('/hostname', methods=['PUT'])
def update_hostname():
    new_hostname = request.json.get('new_hostname')
    return jsonify(post_hostname(new_hostname))

if __name__ == '__main__':
    app.run(debug=True)
