# de 
# https://www.yaklin.ca/2021/08/25/snmp-queries-with-python.html
# Canvio host i community data per un dels hosts que ofereix PySNMP per fer proves.
#

import sys
from pysnmp.entity.rfc3413.oneliner import cmdgen

SYSNAME = '1.3.6.1.2.1.1.5.0'

host = 'demo.pysnmp.com'
snmp_ro_comm = 'public'

# Define a PySNMP CommunityData object named auth, by providing the SNMP community string
auth = cmdgen.CommunityData(snmp_ro_comm)

# Define the CommandGenerator, which will be used to send SNMP queries
cmdGen = cmdgen.CommandGenerator()

# Query a network device using the getCmd() function, providing the auth object, a UDP transport
# our OID for SYSNAME, and don't lookup the OID in PySNMP's MIB's
errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    auth,
    cmdgen.UdpTransportTarget((host, 161)),
    cmdgen.MibVariable(SYSNAME),
    lookupMib=False,
)

# Check if there was an error querying the device
if errorIndication:
    sys.exit()

# We only expect a single response from the host for sysName, but varBinds is an object
# that we need to iterate over. It provides the OID and the value, both of which have a
# prettyPrint() method so that you can get the actual string data
for oid, val in varBinds:
    print(oid.prettyPrint(), val.prettyPrint())
