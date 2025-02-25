# Python-snmp
Apunts i proves sobre l'ús de llibreries Python per implementar el protocol SNMP.

## Recursos
[SNMP MIBs & SNMP OIDs explained](https://www.comparitech.com/net-admin/snmp-mibs-oids-explained/)

[SNMP Library for Python 7.1.16](https://docs.lextudio.com/pysnmp/v7.1/docs/)

[Buscador de MIBs](https://mibbrowser.online/mibdb_search.php)

[SNMP command tools for Linux](https://docs.lextudio.com/snmpclitools/)

[OIDs de Linux](http://www.debianadmin.com/linux-snmp-oids-for-cpumemory-and-disk-statistics.html)

## Test: Comandes per fer consultes. Linux as an agent

### Linux as an agent

#### Pas 1. Configurem el dimoni snmpd

He instal·lat el paquet `snmpd` en una màquina vuirtual Ubuntu Server 24.04 i he modificat algun paràmetre de la configuració per a que poguès escoltar peticions de la xarxa local.

![alt text](image.png)

![alt text](image-1.png)

He afegit a ferro la ip per la que vull que escolti l'agent. També puc afegir la línea 

```bash
agentaddress UDP:161
```

això farà que escolti per totes les interfícies en el port udp 161.

Després, vaig a afegir la següent línea per poder veure la taula d'interfícies:

```bash
###########################################################################
# SECTION: Access Control Setup
#
#   This section defines who is allowed to talk to your running
#   snmp agent.

# Views 
#   arguments viewname included [oid]

#  system + hrSystem groups only
view   systemonly  included   .1.3.6.1.2.1.1
view   systemonly  included   .1.3.6.1.2.1.25.1
#  Juan - afegeixo taula d'interfícies
view   systemonly  included   .1.3.6.1.2.1.2
```

Si el que vull és poder veure-ho tot (per fer proves, per exemple), he de reemplaçar aquestes directives `view` per aquesta altra:

```bash
view   allview    included   .1
```

i reemplaçar la directiva `rocommunity` per 

```bash
rocommunity  public  default -V allview
```

Vaig a fer proves de moment amb SNMPv1 i SNMPv2c en mode només lectura:

![alt text](image-2.png)

Finalment, fem un `$ sudo systemctl restart snmpd.service`.

![alt text](image-3.png)

#### Pas 2. Instal·lem i configurem el client

```bash
$ sudo apt install snmp
```

Aquest paquet et permet de fer consultes a un agent. Si volem treballar amb noms i no directament amb OID, hem d'instal·lar també els MiB en el client, de cara a poder tenir l'estructura de la base de dades i els noms simbòlics dels objectes (OID) de la taula:

```bash
$ sudo apt install snmp-mibs-downloader
```

I comentar també la directiva `mibs` a `/etc/snmp/snmp.conf`:

```bash
# mibs: 
```

### Taula vs branca a OID

Una branca és qualsevol subnivell dins de l'OID jeràrquic i taula és una estructura de fil·les i columnes dins d'una branca. Per exemple, la taula `ifTable` (1.3.6.1.2.1.2.2), que té tantes fil·les com interfícies (en el cas de més avall, 3 interfícies), i que per columnes, té, per exemple:

    * `ifIndex` - **1.3.6.1.2.1.2.2.1.1**
    * `ifDescr` - **1.3.6.1.2.1.2.2.1.2**
    * `ifType`  - **1.3.6.1.2.1.2.2.1.3**


### Exemple de comandes

Totes les comandes tenen unes opcions genèriques d'entrada i de sortida (OID input, `-I`; OID output, `-O`) que es descriuen al manual de `snmpcmd` (`man snmpcmd`).

#### snmpget

Demano el valor escalar de sysUpTime traient el tipus de format (`-OQ`)

```bash
$ snmpget -v2C -c public 192.168.56.101 -OQ sysUpTime.0
DISMAN-EVENT-MIB::sysUpTimeInstance = 0:0:31:15.06
```

Sense l'opció:

```bash
$ snmpget -v2C -c public 192.168.56.101 sysUpTime.0
DISMAN-EVENT-MIB::sysUpTimeInstance = Timeticks: (307481) 0:51:14.81
```

#### snmpwalk

Recorre taules i branques.

`snmpwalk` - recorre tota una branca de OIDs.

1. Llistat de totes les interfícies d'un agent (en aquest cas, Linux):

```bash
$ joan@super-ThinkBook-14-G4-IAP:~$ snmpwalk -v2c -c public 192.168.56.101 1.3.6.1.2.1.2.2.1.2
IF-MIB::ifDescr.1 = STRING: lo
IF-MIB::ifDescr.2 = STRING: enp0s3
IF-MIB::ifDescr.3 = STRING: enp0s8
```

2. Llistat de tota la branca/taula d'interfícies:

```bash
$ snmpwalk -v2c -c public 192.168.56.101 1.3.6.1.2.1.2.2
IF-MIB::ifNumber.0 = INTEGER: 3
IF-MIB::ifIndex.1 = INTEGER: 1
IF-MIB::ifIndex.2 = INTEGER: 2
IF-MIB::ifIndex.3 = INTEGER: 3
IF-MIB::ifDescr.1 = STRING: lo
IF-MIB::ifDescr.2 = STRING: enp0s3
IF-MIB::ifDescr.3 = STRING: enp0s8
IF-MIB::ifType.1 = INTEGER: softwareLoopback(24)
IF-MIB::ifType.2 = INTEGER: ethernetCsmacd(6)
IF-MIB::ifType.3 = INTEGER: ethernetCsmacd(6)
IF-MIB::ifMtu.1 = INTEGER: 65536
IF-MIB::ifMtu.2 = INTEGER: 1500
IF-MIB::ifMtu.3 = INTEGER: 1500
IF-MIB::ifSpeed.1 = Gauge32: 10000000
IF-MIB::ifSpeed.2 = Gauge32: 1000000000
IF-MIB::ifSpeed.3 = Gauge32: 1000000000
IF-MIB::ifPhysAddress.1 = STRING: 
IF-MIB::ifPhysAddress.2 = STRING: 8:0:27:e:26:3e
IF-MIB::ifPhysAddress.3 = STRING: 8:0:27:ca:45:f2
IF-MIB::ifAdminStatus.1 = INTEGER: up(1)
IF-MIB::ifAdminStatus.2 = INTEGER: up(1)
IF-MIB::ifAdminStatus.3 = INTEGER: up(1)
IF-MIB::ifOperStatus.1 = INTEGER: up(1)
IF-MIB::ifOperStatus.2 = INTEGER: up(1)
IF-MIB::ifOperStatus.3 = INTEGER: up(1)
IF-MIB::ifLastChange.1 = Timeticks: (0) 0:00:00.00
IF-MIB::ifLastChange.2 = Timeticks: (802075) 2:13:40.75
IF-MIB::ifLastChange.3 = Timeticks: (0) 0:00:00.00
IF-MIB::ifInOctets.1 = Counter32: 28946
IF-MIB::ifInOctets.2 = Counter32: 5850598
IF-MIB::ifInOctets.3 = Counter32: 29417
IF-MIB::ifInUcastPkts.1 = Counter32: 342
IF-MIB::ifInUcastPkts.2 = Counter32: 60926
IF-MIB::ifInUcastPkts.3 = Counter32: 191
IF-MIB::ifInNUcastPkts.1 = Counter32: 0
IF-MIB::ifInNUcastPkts.2 = Counter32: 0
IF-MIB::ifInNUcastPkts.3 = Counter32: 0
IF-MIB::ifInDiscards.1 = Counter32: 0
IF-MIB::ifInDiscards.2 = Counter32: 0
IF-MIB::ifInDiscards.3 = Counter32: 0
IF-MIB::ifInErrors.1 = Counter32: 0
IF-MIB::ifInErrors.2 = Counter32: 0
IF-MIB::ifInErrors.3 = Counter32: 0
IF-MIB::ifInUnknownProtos.1 = Counter32: 0
IF-MIB::ifInUnknownProtos.2 = Counter32: 0
IF-MIB::ifInUnknownProtos.3 = Counter32: 0
IF-MIB::ifOutOctets.1 = Counter32: 28946
IF-MIB::ifOutOctets.2 = Counter32: 6176354
IF-MIB::ifOutOctets.3 = Counter32: 19507
IF-MIB::ifOutUcastPkts.1 = Counter32: 342
IF-MIB::ifOutUcastPkts.2 = Counter32: 60976
IF-MIB::ifOutUcastPkts.3 = Counter32: 216
IF-MIB::ifOutNUcastPkts.1 = Counter32: 0
IF-MIB::ifOutNUcastPkts.2 = Counter32: 0
IF-MIB::ifOutNUcastPkts.3 = Counter32: 0
IF-MIB::ifOutDiscards.1 = Counter32: 0
IF-MIB::ifOutDiscards.2 = Counter32: 0
IF-MIB::ifOutDiscards.3 = Counter32: 0
IF-MIB::ifOutErrors.1 = Counter32: 0
IF-MIB::ifOutErrors.2 = Counter32: 0
IF-MIB::ifOutErrors.3 = Counter32: 0
IF-MIB::ifOutQLen.1 = Gauge32: 0
IF-MIB::ifOutQLen.2 = Gauge32: 0
IF-MIB::ifOutQLen.3 = Gauge32: 0
IF-MIB::ifSpecific.1 = OID: SNMPv2-SMI::zeroDotZero
IF-MIB::ifSpecific.2 = OID: SNMPv2-SMI::zeroDotZero
IF-MIB::ifSpecific.3 = OID: SNMPv2-SMI::zeroDotZero
```

#### snmpbulkget

Serveix per demanar més d'una variable OID en una petició. Es poden demanar en la mateixa petició valors escalars (non-repeaters) i valors que estan continguts en taules. Exemple de crida: 

`snmpbulkget -v2c -c public -Cn2 -Cr9 192.168.56.101 1.3.6.1.2.1.1.3 1.3.6.1.2.1.1.5 1.3.6.1.2.1.2.2`. 

Apareixen dos paràmetres nous: `-Cn`, per especificar el nombre de variables non-repeaters que es demanen, i `-Cr` per especificar els valors que es volen obtenir d'una taula. Després d'aquestes opcions apareixen els OID que es volen recollir. En l'exemple, els dos primers seràn els escalars i el tercer OID és una taula (la taula d'interfícies `ifTable`) de la qual es volen agafar 9 valors.

```bash
joan@super-ThinkBook-14-G4-IAP:~$ snmpbulkget -v2c -c public -Cn2 -Cr9 192.168.56.101 1.3.6.1.2.1.1.3 1.3.6.1.2.1.1.5 1.3.6.1.2.1.2.2
DISMAN-EVENT-MIB::sysUpTimeInstance = Timeticks: (145445) 0:24:14.45
SNMPv2-MIB::sysName.0 = STRING: joshua
IF-MIB::ifIndex.1 = INTEGER: 1
IF-MIB::ifIndex.2 = INTEGER: 2
IF-MIB::ifIndex.3 = INTEGER: 3
IF-MIB::ifDescr.1 = STRING: lo
IF-MIB::ifDescr.2 = STRING: enp0s3
IF-MIB::ifDescr.3 = STRING: enp0s8
IF-MIB::ifType.1 = INTEGER: softwareLoopback(24)
IF-MIB::ifType.2 = INTEGER: ethernetCsmacd(6)
IF-MIB::ifType.3 = INTEGER: ethernetCsmacd(6)
```

#### snmpbulkwalk

#### snmpgetnext

#### snmpnetstat

#### snmpnetstat

#### snmpstatus

#### snmptable

#### snmptest

#### snmptrap

#### snmptranslate

Tradueix OIDs a mode numèric o viceversa (a mode textual). Ho fa en base a MIBs que pots passar com a arguments a la mateixa comanda o a través dels MIBs que puguis tenir instal·lats. 

Sense opcions extres, li has de passar tota la ruta del OID:

```bash
joan@super-ThinkBook-14-G4-IAP:~$ snmptranslate sysDescr
sysDescr: Unknown Object Identifier (Sub-id not found: (top) -> sysDescr)

joan@super-ThinkBook-14-G4-IAP:~$ snmptranslate .iso.org.dod.internet.mgmt.mib-2.system.sysDescr
SNMPv2-MIB::sysDescr
```

Per defecte, et mostra el MIB, que és el mateix que passar-li l'opció `-OS`. Amb l'opció `-On` et tradueix a format numèric:

```bash
$ snmptranslate -On .iso.org.dod.internet.mgmt.mib-2.system.sysDescr
.1.3.6.1.2.1.1.1
```

Amb l'opció -IR no cal passar tota la ruta ja que la comanda et fa una búsqueda massiva del nom:

```bash
$ snmptranslate -IR sysDescr
SNMPv2-MIB::sysDescr
```

Si volem que ens mostri tot el camí:

```bash
$ snmptranslate -Of -IR sysDescr
.iso.org.dod.internet.mgmt.mib-2.system.sysDescr
```

Si vols una descripció detallada de l'OID, pots fer servir l'opció `-Td`:

```bash
$ snmptranslate -Td -OS -IR system.sysDescr
SNMPv2-MIB::sysDescr
sysDescr OBJECT-TYPE
  -- FROM	SNMPv2-MIB
  -- TEXTUAL CONVENTION DisplayString
  SYNTAX	OCTET STRING (0..255) 
  DISPLAY-HINT	"255a"
  MAX-ACCESS	read-only
  STATUS	current
  DESCRIPTION	"A textual description of the entity.  This value should
            include the full name and version identification of
            the system's hardware type, software operating-system,
            and networking software."
::= { iso(1) org(3) dod(6) internet(1) mgmt(2) mib-2(1) system(1) 1 }
```

i amb l'opció `-Tp` et mostra tota la branca en format arbre:

```bash
$ snmptranslate -Tp -OS -IR system
+--system(1)
   |
   +-- -R-- String    sysDescr(1)
   |        Textual Convention: DisplayString
   |        Size: 0..255
   +-- -R-- ObjID     sysObjectID(2)
   +-- -R-- TimeTicks sysUpTime(3)
   |  |
   |  +--sysUpTimeInstance(0)
   |
   +-- -RW- String    sysContact(4)
   |        Textual Convention: DisplayString
   |        Size: 0..255
   +-- -RW- String    sysName(5)
   |        Textual Convention: DisplayString
   |        Size: 0..255
   +-- -RW- String    sysLocation(6)
   |        Textual Convention: DisplayString
   |        Size: 0..255
   +-- -R-- INTEGER   sysServices(7)
   |        Range: 0..127
   +-- -R-- TimeTicks sysORLastChange(8)
   |        Textual Convention: TimeStamp
   |
   +--sysORTable(9)
      |
      +--sysOREntry(1)
         |  Index: sysORIndex
         |
         +-- ---- INTEGER   sysORIndex(1)
         |        Range: 1..2147483647
         +-- -R-- ObjID     sysORID(2)
         +-- -R-- String    sysORDescr(3)
         |        Textual Convention: DisplayString
         |        Size: 0..255
         +-- -R-- TimeTicks sysORUpTime(4)
                  Textual Convention: TimeStamp
```

Llistar tots els OID:

```bash
$ snmptranslate -To
.1.3
.1.3.6
.1.3.6.1
.1.3.6.1.1
.1.3.6.1.2
.1.3.6.1.2.1
.1.3.6.1.2.1.1
.1.3.6.1.2.1.1.1
.1.3.6.1.2.1.1.2
.1.3.6.1.2.1.1.3
.1.3.6.1.2.1.1.3.0
.1.3.6.1.2.1.1.4
.1.3.6.1.2.1.1.5
.1.3.6.1.2.1.1.6
.1.3.6.1.2.1.1.7
...

$ snmptranslate -Tl | head
.iso(1).org(3)
.iso(1).org(3).dod(6)
.iso(1).org(3).dod(6).internet(1)
.iso(1).org(3).dod(6).internet(1).directory(1)
.iso(1).org(3).dod(6).internet(1).mgmt(2)
.iso(1).org(3).dod(6).internet(1).mgmt(2).mib-2(1)
.iso(1).org(3).dod(6).internet(1).mgmt(2).mib-2(1).system(1)
.iso(1).org(3).dod(6).internet(1).mgmt(2).mib-2(1).system(1).sysDescr(1)
.iso(1).org(3).dod(6).internet(1).mgmt(2).mib-2(1).system(1).sysObjectID(2)
.iso(1).org(3).dod(6).internet(1).mgmt(2).mib-2(1).system(1).sysUpTime(3)
```

## Creació de l'entorn Python

Genero entorn virtual (*Python Virtual Environment*) i l'activo:

```bash
$ python -m venv .venv
$ source .venv/bin/activate
```
Instal·lo el paquet [pysnmp](https://github.com/lextudio/pysnmp):

```bash
$ pip install pysnmp
Collecting pysnmp
  Downloading pysnmp-7.1.16-py3-none-any.whl.metadata (4.3 kB)
Collecting pyasn1!=0.5.0,>=0.4.8 (from pysnmp)
  Downloading pyasn1-0.6.1-py3-none-any.whl.metadata (8.4 kB)
Downloading pysnmp-7.1.16-py3-none-any.whl (340 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 341.0/341.0 kB 1.4 MB/s eta 0:00:00
Downloading pyasn1-0.6.1-py3-none-any.whl (83 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 83.1/83.1 kB 2.4 MB/s eta 0:00:00
Installing collected packages: pyasn1, pysnmp
Successfully installed pyasn1-0.6.1 pysnmp-7.1.16
```
Paquets instal·lats:

```bash
$ pip freeze
pyasn1==0.6.1
pysnmp==7.1.16
```

## Primer test

A *v1-get.py* hi ha un primer script que fa un get sobre un dispositiu de demo. La sortida:

```bash
$ python3 v1-get.py 
SNMPv2-MIB::sysDescr.0 = #SNMP Agent on .NET Standard
```

## Projecte

### Tasques

  1. ~~Obtenir i provar una sèrie de paràmetres escalars a agent Linux~~
  2. ~~Llegir article sobre MiB/OID~~
  3. Principals queries snmp (snmpwalk, ...) i diferències entre elles.
  4. Obtenir i provar una sèrie de paràmetres tabulars a agent Linux
  5. Com fer servir snmptranslate
  6. Traps
  7. PySNMP. Generar tots els scripts a Python (snmpwalk, ...)
  8. Llistat de paràmetres escalars i tabulars - Cisco
  9. Llistat de paràmetres escalars i tabulars - Mikrotik
  10. Temporitzar Projecte
  11. Document - enunciat del projecte
  12. Rúbrica d'avaluació
  13. Anar preparant les classes i el desenvolupament del projecte

### Opció 1: Fer un MiB browser online.

Podríem implementar un MiB per Linux, un per Cisco i un per Mikrotik. Ens podríem instal·lar un browser per veure quin aspecte té i les seves funcionalitats i després intentar implementar-lo a nivell de web. Podríem fer funcionalitats com les últimes accions comeses, els últims get, una pàgina amb les notificacions o amb els traps. Passos:

  0. Primeres passes amb Python.
  1. Primeres passes amb Flask. Creació d'entorns virtuals Python. Instal·lació de Flask i de PySNMP. Rutes amb Flask. Jinja2
    1.0. Entrenaments creant rutes. Fent servir Jinja2.
    1.1. Entrenament - connectar a BBDD?
  2. SNMP. Teoria. Pràctica SNMP a Cisco Packet Tracer. Obtenir escalars i taules. 
    2.0. Afegir a teoria MiB / OID (Mirar l'enllaç que tenim)
    2.1. Afegir que trobin els OID que podran fer servir en el projecte
    2.2. Afegir de trobar dades tabulars?
  3. SNMP en entorn real (Agent Linux? Cisco? Mikrotik?). Instal·lació d'un MiB browser. Paquet snmp a Linux. Paquet snmpd a Linux per instal·lar agent. Obtenir escalars i taules.
    3.1. [SNMP commands](https://docs.lextudio.com/snmpclitools/)
    3.2. Obtenir llistat de OID a Linux i a Mikrotik
  4. PySNMP. Exemple d'escrips de consultes. Explicació.
  5. Desenvolupament 1 - Pàgina que demana dades per fer una consulta get a un agent. Resposta a nova pàgina. Podem escollir agent, tipus de consulta.
  6. Desenvolumament 2 - Fiquem resposta a una base de dades. Relacional? XML? ...?
  7. Desenvolupament 3 - Respostes es mostren en una nova fulla.
  8. Altres: SNMPv3, Alguna funcionalitat extra a la web (explorar / afegir agents, ...)

