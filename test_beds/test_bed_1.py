# ===================================== DUT 1 declaration =====================================


DUT1Ports = {'v1':  'extreme-ethernet 0/1',   'v1speed': "1000", 'v1value': 'Ex0/1',
             'v2':  'extreme-ethernet 0/2',   'v2speed': "1000", 'v2value': 'Ex0/2',
             'x1':  'gigabitethernet 0/9',   'x1speed': "1000", 'x1value': 'Gi0/9',
             'x2':  'gigabitethernet 0/10',  'x2speed': "1000", 'x2value': 'Gi0/10',
             'h1':  'gigabitethernet 0/21',   'h1speed': "1000", 'h1value': 'Gi0/21',
             'h2': 'gigabitethernet 0/22',   'h2speed': "1000", 'h2value': 'Gi0/22' }

DUT1 = {
            'ip': "10.2.109.198",
            'user': 'admin',
            'password': 'Admin1234!',
            'connectionObject': 'telnet',
            'terminal_ip': '10.2.109.9',
            'terminal_port': 6026,
            'ports': DUT1Ports,
            'model': 'EX2028-P',
            'version': '5.0.2-r2',
            'hostname': 'Andrei-2028',
            'mac_address': '00:01:01:01:39:01', }

# ===================================== DUT 2 declaration =====================================

DUT2Ports = {'h1':  'gigabitethernet 0/3',   'h1speed': "1000", 'h1value': 'Gi0/5',
             'h2':  'gigabitethernet 0/4',   'h2speed': "1000", 'h2value': 'Gi0/6',
             'h3':  'gigabitethernet 0/1',   'h3speed': "1000", 'h3value': 'Gi0/1',
             'v1':  'gigabitethernet 0/9',   'v1speed': "1000", 'v1value': 'Gi0/9',
             'v2':  'gigabitethernet 0/10',  'v2speed': "1000", 'v2value': 'Gi0/10' }

DUT2 = {
            'ip': "10.2.109.172",
            'user': 'admin',
            'password': 'Admin1234!',
            'connectionObject': 'telnet',
            'terminal_ip': '10.2.109.9',
            'terminal_port': 6006,
            'ports': DUT2Ports,
            'model': 'EX2010-P',
            'version': '5.0.2-r2',
            'hostname': 'Andrei-2010',
            'mac_address': '00:01:01:01:49:01', }


# ===================================== DUT 3 declaration =====================================

DUT3Ports = {'h1':  'gigabitethernet 0/3',   'h1speed': "1000", 'h1value': 'Gi0/5',
             'h2':  'gigabitethernet 0/4',   'h2speed': "1000", 'h2value': 'Gi0/6',
             'h3':  'gigabitethernet 0/11',   'h3speed': "1000", 'h3value': 'Gi0/11',
             'x1':  'gigabitethernet 0/9',   'x1speed': "1000", 'x1value': 'Gi0/9',
             'x2':  'gigabitethernet 0/10',  'x2speed': "1000", 'x2value': 'Gi0/10' }

DUT3 = {
            'ip': "10.2.109.98",
            'user': 'admin',
            'password': 'Admin1234!',
            'connectionObject': 'telnet',
            'terminal_ip': '10.2.109.9',
            'terminal_port': 6010,
            'ports': DUT3Ports,
            'model': 'EX3052R-P',
            'version': '5.0.2-r2',
            'hostname': 'Andrei-3052',
            'mac_address': 'bc:e6:7c:a5:89:01' }

# ===================================== DUT 4 declaration =====================================

DUT4Ports = {'h1':  'gigabitethernet 0/11',   'h1speed': "1000", 'h1value': 'Gi0/11',
             'v1':  'gigabitethernet 0/9',    'v1speed': "1000", 'v1value': 'Gi0/9',
             'v2':  'gigabitethernet 0/3',   'v2speed': "1000", 'v2value': 'Gi0/9',
             'v3':  'gigabitethernet 0/4',   'v3speed': "1000", 'v3value': 'Gi0/10',
             'v4':  'extreme-ethernet 0/1',   'v4speed': "10000", 'v4value': 'Ex0/1',
             'v5':  'extreme-ethernet 0/2',  'v5speed': "10000", 'v5value': 'Ex0/2',
             'v6':  'extreme-ethernet 0/3',  'v6speed': "10000", 'v6value': 'Ex0/3',
             'x1':  'gigabitethernet 0/1',  'x1speed': "1000", 'x1value': 'Gi0/1' }

DUT4 = {
            'ip': "10.2.109.118",
            'user': 'admin',
            'password': 'Admin1234!',
            'connectionObject': 'telnet',
            'terminal_ip': '10.2.109.9',
            'terminal_port': 6010,
            'ports': DUT4Ports,
            'model': 'EX2028-P',
            'version': '5.0.2-r4',
            'hostname': 'new1',
            'mac_address': '58:c1:7a:ec:94:41' }

# ===================================== DUT 4 declaration =====================================

DUT5Ports = {'h1':  'gigabitethernet 0/25',   'h1speed': "1000", 'h1value': 'Gi0/25',
             'v1':  'gigabitethernet 0/26',   'v1speed': "1000", 'v1value': 'Gi0/26',
             'v2':  'gigabitethernet 0/3',    'v2speed': "1000", 'v2value': 'Gi0/9',
             'v3':  'gigabitethernet 0/4',    'v3speed': "1000", 'v3value': 'Gi0/10',
             'v4':  'extreme-ethernet 0/3',   'v4speed': "10000", 'v4value': 'Ex0/3',
             'v5':  'extreme-ethernet 0/4',   'v5speed': "10000", 'v5value': 'Ex0/4',
             'x1':  'extreme-ethernet 0/2',   'x1speed': "1000)", 'x1value': 'Ex0/2' }

DUT5 = {
            'ip': "10.2.109.241",
            'user': 'admin',
            'password': 'Admin1234!',
            'connectionObject': 'telnet',
            'terminal_ip': '10.2.109.9',
            'terminal_port': 6010,
            'ports': DUT5Ports,
            'model': 'EX2052',
            'version': '5.0.2-r4',
            'hostname': 'cip52',
            'mac_address': '58:c1:7a:ec:05:81' }

# ===================================== DUT 6 declaration =====================================

DUT6Ports = {'h1':  'extreme-ethernet 0/1',   'h1speed': "10000", 'h1value': 'Ex0/1',
             'x1':  'extreme-ethernet 0/22',   'x1speed': "10000", 'x1value': 'Ex0/22',
             'x2':  'extreme-ethernet 0/23',  'x2speed': "10000", 'x2value': 'Ex0/23',
             'v1': 'extreme-ethernet 0/9', 'v1speed': "10000", 'v1value': 'Ex0/9',
             'v2': 'extreme-ethernet 0/10', 'v2speed': "10000", 'v2value': 'Ex0/10',
             'v3': 'extreme-ethernet 0/11', 'v3speed': "10000", 'v3value': 'Ex0/11',
             'v4': 'extreme-ethernet 0/12', 'v4speed': "10000", 'v4value': 'Ex0/12' }

DUT6 = {
            'ip': "10.2.109.110",
            'user': 'admin',
            'password': 'Admin1234!',
            'connectionObject': 'telnet',
            'terminal_ip': '10.2.109.9',
            'terminal_port': 6025,
            'ports': DUT6Ports,
            'model': 'EX3024F',
            'version': '6.0.0-e44',
            'hostname': 'FA2',
            'mac_address': '30:cb:c7:ce:91:81' }


# ===================================== DUT Test Flavia declaration =====================================

DUTFPorts = {'h1':  'gigabitethernet 0/2',   'h1speed': "1000", 'h1value': 'Gi0/5', }

DUTF = {
            'ip': "10.2.109.80",
            'user': 'admin',
            'password': 'Admin1234!',
            'connectionObject': 'telnet',
            'terminal_ip': '10.2.109.9',
            'terminal_port': 6025,
            'ports': DUT6Ports,
            'model': '',
            'version': '',
            'hostname': '',
            'mac_address': '' }

# def test_func_1():
#
#     print(DUT1["ports"]["v1"])
#     print(DUT1["ports"]["v1value"])
#     print(DUT1["ip"])
#
#     print(DUT2["ports"]["v1"])
#     print(DUT2["ports"]["v1value"])
#     print(DUT2["ip"])
#
#     print(DUT3["ports"]["x1"])
#     print(DUT3["ports"]["x1value"])
#     print(DUT3["ip"])








