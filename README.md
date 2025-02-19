# Python-snmp
Apunts i proves sobre l'ús de llibreries Python per implementar el protocol SNMP.

## Recursos
[SNMP MIBs & SNMP OIDs explained](https://www.comparitech.com/net-admin/snmp-mibs-oids-explained/)
[SNMP Library for Python 7.1.16](https://docs.lextudio.com/pysnmp/v7.1/docs/)
[Buscador de MIBs](https://mibbrowser.online/mibdb_search.php)
[SNMP command tools for Linux](https://docs.lextudio.com/snmpclitools/)

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

## Alguns apunts sobre SNMP

### MiB
Hi han molts tipus de MiB. Cada MiB té els seus propis OIDs. Hi han MiB per Cisco, per Linux, per Mikrotik, MiB que engloben uns tipus de dades, etc.

## Test: Comandes per fer consultes. Linux as an agent

### Linux as an agent

He instal·lat el paquet `snmpd` en una màquina vuirtual Ubuntu Server 24.04 i he modificat algun paràmetre de la configuració per a que poguès escoltar peticions de la xarxa local.

![alt text](image.png)

![alt text](image-1.png)

Vaig a fer proves de moment amb SNMPv1 i SNMPv2c en mode només lectura:

![alt text](image-2.png)

Finalment, fem un `$ sudo systemctl reload snmpd.service`.

![alt text](image-3.png)

## Projecte

### Opció 1: Fer un MiB browser online.

Podríem implementar un MiB per Linux, un per Cisco i un per Mikrotik. Ens podríem instal·lar un browser per veure quin aspecte té i les seves funcionalitats i després intentar implementar-lo a nivell de web. Podríem fer funcionalitats com les últimes accions comeses, els últims get, una pàgina amb les notificacions o amb els traps. Passos:

  0. Primeres passes amb Python.
  1. Primeres passes amb Flask. Creació d'entorns virtuals Python. Instal·lació de Flask i de PySNMP. Rutes amb Flask. Jinja2
  2. SNMP. Teoria. Pràcctica SNMP a Cisco Packet Tracer. Obtenir escalars i taules. 
  3. SNMP en entorn real (Agent Linux? Cisco? Mikrotik?). Instal·lació d'un MiB browser. Paquet snmp a Linux. Paquet snmpd a Linux per instal·lar agent. Obtenir escalars i taules.
    3.1. [SNMP commands](https://docs.lextudio.com/snmpclitools/)
  4. PySNMP. Exemple d'escrips de consultes. Explicació.
  5. Desenvolupament 1 - Pàgina que demana dades per fer una consulta get a un agent. Resposta a nova pàgina. Podem escollir agent, tipus de consulta.
  6. Desenvolumament 2 - Fiquem resposta a una base de dades. Relacional? XML? ...?
  7. Desenvolupament 3 - Respostes es mostren en una nova fulla.

