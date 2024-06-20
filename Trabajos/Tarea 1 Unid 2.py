import json
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
    {'name':'Router_1',
     'service':'WEB',
     'remote_conection':'SSH',
     'linux distribution':'Ubuntu'
                }],
    'router2':[
    {'name':'Router_2',
     'service1':'DNS',
     'service2':'WEB',
     'linux distribution':'Linux'
                }],
    'router3':[
    {'name':'Router_3',
     'service1':'FTP',
     'service2':'DHCP',
     'linux distribution':'Centos 8'
                }]
    }

print(json.dumps(dic_data, indent=2))
print(json.dumps(dic_data2, indent=3))

if __name__ == '__main__':
    pass