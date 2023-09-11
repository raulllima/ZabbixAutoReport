from scrippy_snmp.snmp import Snmp

HOST = "172.17.4.75"
PORT = 161
RO_COMMUNITY = "public"
RW_COMMUNITY = "public"
VERSION = "2c"

snmp = Snmp(host=HOST, port=PORT, community=RO_COMMUNITY, version=VERSION)

LOCATION_OID = ".1.3.6.1.2.1.25"

snmp = Snmp(host=HOST, port=PORT, community=RO_COMMUNITY, version=VERSION)
location = snmp.get(LOCATION_OID)

print(location)