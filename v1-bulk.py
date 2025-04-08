import asyncio
from pysnmp.hlapi.v3arch.asyncio import *


async def run():
    snmpEngine = SnmpEngine()

    iterator = bulk_cmd(
        snmpEngine,
        CommunityData("public", mpModel=1),
        await UdpTransportTarget.create(("192.168.56.101", 161)),
        ContextData(),
        1, 
        1, 
        # ObjectType(ObjectIdentity('1.3.6.1.2.1.1.3')),
        ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1')),
        ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2'))
    )

    errorIndication, errorStatus, errorIndex, varBinds = await iterator

    if errorIndication:
        print(errorIndication)

    elif errorStatus:
        print(
            "{} at {}".format(
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
            )
        )
    else:
        for varBind in varBinds:
            print(" = ".join([x.prettyPrint() for x in varBind]))

    snmpEngine.close_dispatcher()


asyncio.run(run())