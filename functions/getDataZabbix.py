import requests

class getDataZabbix():
    def __init__(self, zabbixApiURL, zabbixApiUser, zabbixApiPass):
        self.zabbixApiURL = zabbixApiURL
        self.session = requests.Session()

        self.auth_token = self.session.post(self.zabbixApiURL, json={
            'jsonrpc': '2.0',
            'method': 'user.login',
            'params': {
                'user': zabbixApiUser,
                'password': zabbixApiPass
            },
            'id': 1
        }).json()['result']

    def getGroups(self):
        pass

    def getHosts(self, groupID):
        return self.session.post(self.zabbixApiURL, json={
            'jsonrpc': '2.0',
            'method': 'host.get',
            'params': {
                'output': ['hostid', 'host'],
                'groupids': groupID,
                'sortfield': 'host',
                'filter': {
                    'status': 0
                }
            },
            'auth': self.auth_token,
            'id': 3
        }).json()['result']
    
    def getItems(self, hostID, objKey=None):
        items = []
        itemsRaw = self.session.post(self.zabbixApiURL, json={
            'jsonrpc': '2.0',
            'method': 'item.get',
            'params': {
                'output': ['itemid', 'name', 'key_'],
                'hostids': hostID,
                'sortfield': 'name',
                'search': {
                    "key_": objKey
                },
                'filter': {
                    'status': 0
                }
            },
            'auth': self.auth_token,
            'id': 3
        }).json()['result']
        
        for item in itemsRaw:

            if (',pused]' in item['key_']):
                items.append(item)
            elif ('system.cpu.util' in item['key_'] and 'CPU utilization' in item['name']):
                if ('system.cpu.util[snmp]' in item['key_']):
                    items.append(item)
                    break
                else:
                    items.append(item)
            elif ('vm.memory.util' in item['key_']):
                items.append(item)

        return items
    
    def getHistory(self, itemID, itemName=None):
        dataPerHost = []
        response = self.session.post(self.zabbixApiURL, json={
            'jsonrpc': '2.0',
            'method': 'history.get',
            'params': {
                'output': 'extend',
                'history': 0,  # 0 para valores numéricos
                'itemids': itemID,
                'sortfield': 'clock',
                'sortorder': 'DESC',
                'limit': 1
            },
            'auth': self.auth_token,
            'id': 4
        }).json()['result']

        if (response):
            value = response[0]['value']
            dataPerHost.append(f"{float(value):.2f}%")
        else:
            dataPerHost.append("Collector not working!")

        return dataPerHost
