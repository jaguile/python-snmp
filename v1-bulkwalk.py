import asyncio
from pysnmp.hlapi.v3arch.asyncio import *

"""
Bulk walk MIB
+++++++++++++

Send a series of SNMP GETBULK requests using the following options:

* with SNMPv2c, community 'public'
* over IPv4/UDP
* to an Agent at demo.pysnmp.com:161
* for all OIDs past SNMPv2-MIB::system
* run till end-of-mib condition is reported by Agent
* based on asyncio I/O framework

Functionally similar to:

| $ snmpbulkwalk -v2c -c public -Cn0 -Cr50 \
|                demo.pysnmp.com  SNMPv2-MIB::system

"""  

async def run():
    snmpEngine = SnmpEngine()

    print ("Vaig a fer un bulk walk")
    objects = bulk_walk_cmd(
            snmpEngine,
            CommunityData("public"),
            await UdpTransportTarget.create(("192.168.56.101", 161)),
            ContextData(),
            0,
            1,
            ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2')),
            lexicographicMode = False
        )

    async for errorIndication, errorStatus, errorIndex, varBinds in objects:
        if errorIndication:
            print(f"Error: {errorIndication}")
            break
        elif errorStatus:
            print(f"{errorStatus.prettyPrint()} at {errorIndex}")
            break
        else:
            for varBind in varBinds:
                print(" = ".join([x.prettyPrint() for x in varBind]))
    
    snmpEngine.close_dispatcher()


asyncio.run(run())