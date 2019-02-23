Python Server for Torque Pro
============================

This is a server that receives uploaded logging from the Android Torque Pro app
and then publishes it to an InfluxDB database.

I have a Bolt EV, so this includes support for many Bolt specific PIDs.

[Bolt EV PIDs](https://docs.google.com/spreadsheets/d/1sY5n8WFu52U6a4_mg3MdcGcmDk3scAP8_muSy-BlXPc/edit#gid=1125667062)

Influx Config
-------------

```
host=localhost
port=6543
user=torquepro
password=secretpassword
database=torquepro
```
