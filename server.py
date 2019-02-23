#!/usr/bin/python3

import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
import datetime

import arrow
import influxdb

HOST_NAME = '0.0.0.0'
PORT_NUMBER = 8432

MAPPINGS = {
    'k224369': 'Charger AC Current',
    'k224368': 'Charger AC Voltage',
    'k22436c': 'Charger HV Current',
    'k22436b': 'Charger HV Voltage',
    'k222414': 'HV Current',
    'k224356': 'HV Current HD',
    'k222885': 'MG Voltage',
    'k221c24': 'MG Voltage 2',
    'k2228cf': 'MG Voltage 3',
    'k2228d0': 'MG Voltage 4',
    'k2228fb': 'MG Voltage 5',
    'k224329': 'MG Voltage 6',
    'k22432d': 'MG Voltage 7',
    'k015b': 'State of Charge Raw',
    'k222411': 'State of Charge Raw 2',
    'k2241a3': 'Battery Capacity',
    'k2243af': 'State Of Charge HD Raw',
    'k228334': 'Battery Level Displayed',
    'k22000d': 'Speed kmh',
    'k22000d': 'Speed mph',
    'k221940': 'Tran Temp',
    'k22437d': 'Last Charge AC Wh',
    'k222889': 'Gear Position',
    'k2241b2': 'Batt Coolant Pump RPM',
    'k2241b4': 'Heater - Cabin',
    'k2241b6': 'Heater - Battery',
    'k22434f': 'Batt Temp',
    'k222416': 'Batt Temp 2416',
    'k222417': 'Batt Temp 2417',
    'k221c26': 'Electronics Temp 1',
    'k221c28': 'Electronics Temp 2',
    'k221c2a': 'Electronics Temp 3',
    'k221c43': 'H2 Electronics Temp',
    'k2282b2': 'ent Temperature?',
    'k221942': 'Trans RPM',
    'k0146': 'Air Temp 0',
    'k22801e': 'Air Temp 1',
    'k22801f': 'Air Temp 2',
    'k22242c': 'Brake Torque',
    'k221564': 'AC High Side Pressure',
    'k220042': 'M Control Module Voltage',
    'k2224df': 'MG Current ?',
    'k222883': 'MG Other Current ?',
    'k2228de': 'Unknown 2228DE',
    'k2228e1': 'Unknown 2228E1',
    'k2228e4': 'Unknown 2228E4',
    'k2228f1': 'Unknown 2228F1',
    'k2228f2': 'Unknown 2228F2',
    'k2228f4': 'Unknown 2228F4',
    'k2228f8': 'Unknown 2228F8',
    'k2228f9': 'Unknown 2228F9',
    'k2228fe': 'Unknown 2228FE',
    'k222428': 'Unknown 222428',
    'k222429': 'Unknown 222429 HVV',
    'k22242d': 'Unknown 22242D',
    'k222434': 'Unknown 222434',
    'k22288a': 'Unknown 22288A',
    'k224331': 'V 224331',
    'k224332': 'V 224332',
    'k224333': 'V 224333',
    'k22194f': 'Unknown 22194F',
    'k22197e': 'Unknown 22197E',
    'k22433b': 'Interesting 433B',
    'k224357': 'Unknown 224357',
    'k22439c': 'Unknown 22439C',
    'k2241b7': 'Charging Limit ?',
    'k224373': 'L2 Charger Active',
    'k22835a': 'Unknown 22835A',
    'k22433c': 'Unknown 22433C',
    'k2240d3': 'BECM 5V Reference Voltage 1',
    'k2240d4': 'BECM 5V Reference Voltage 2',
    'k2240d7': 'BECM Battery Section 1 Temp',
    'k2240d9': 'BECM Battery Section 2 Temp',
    'k2240db': 'BECM Battery Section 3 Temp',
    'k2240dd': 'BECM Battery Section 4 Temp',
    'k2240df': 'BECM Battery Section 5 Temp',
    'k2240e1': 'BECM Battery Section 6 Temp',
    'k2241a4': 'BECM Battery Coolant Temp ?',
    'k22c218': 'BECM Average Cell Voltage ?',
    'k224181': 'Battery Cell Voltage #01',
    'k224182': 'Battery Cell Voltage #02',
    'k224183': 'Battery Cell Voltage #03',
    'k224184': 'Battery Cell Voltage #04',
    'k224185': 'Battery Cell Voltage #05',
    'k224186': 'Battery Cell Voltage #06',
    'k224187': 'Battery Cell Voltage #07',
    'k224188': 'Battery Cell Voltage #08',
    'k224189': 'Battery Cell Voltage #09',
    'k22418a': 'Battery Cell Voltage #10',
    'k22418b': 'Battery Cell Voltage #11',
    'k22418c': 'Battery Cell Voltage #12',
    'k22418d': 'Battery Cell Voltage #13',
    'k22418e': 'Battery Cell Voltage #14',
    'k22418f': 'Battery Cell Voltage #15',
    'k224190': 'Battery Cell Voltage #16',
    'k224191': 'Battery Cell Voltage #17',
    'k224192': 'Battery Cell Voltage #18',
    'k224193': 'Battery Cell Voltage #19',
    'k224194': 'Battery Cell Voltage #20',
    'k224195': 'Battery Cell Voltage #21',
    'k224196': 'Battery Cell Voltage #22',
    'k224197': 'Battery Cell Voltage #23',
    'k224198': 'Battery Cell Voltage #24',
    'k224199': 'Battery Cell Voltage #25',
    'k22419a': 'Battery Cell Voltage #26',
    'k22419b': 'Battery Cell Voltage #27',
    'k22419c': 'Battery Cell Voltage #28',
    'k22419d': 'Battery Cell Voltage #29',
    'k22419e': 'Battery Cell Voltage #30',
    'k22419f': 'Battery Cell Voltage #31',
    'k224200': 'Battery Cell Voltage #32',
    'k224201': 'Battery Cell Voltage #33',
    'k224202': 'Battery Cell Voltage #34',
    'k224203': 'Battery Cell Voltage #35',
    'k224204': 'Battery Cell Voltage #36',
    'k224205': 'Battery Cell Voltage #37',
    'k224206': 'Battery Cell Voltage #38',
    'k224207': 'Battery Cell Voltage #39',
    'k224208': 'Battery Cell Voltage #40',
    'k224209': 'Battery Cell Voltage #41',
    'k22420a': 'Battery Cell Voltage #42',
    'k22420b': 'Battery Cell Voltage #43',
    'k22420c': 'Battery Cell Voltage #44',
    'k22420d': 'Battery Cell Voltage #45',
    'k22420e': 'Battery Cell Voltage #46',
    'k22420f': 'Battery Cell Voltage #47',
    'k224210': 'Battery Cell Voltage #48',
    'k224211': 'Battery Cell Voltage #49',
    'k224212': 'Battery Cell Voltage #50',
    'k224213': 'Battery Cell Voltage #51',
    'k224214': 'Battery Cell Voltage #52',
    'k224215': 'Battery Cell Voltage #53',
    'k224216': 'Battery Cell Voltage #54',
    'k224217': 'Battery Cell Voltage #55',
    'k224218': 'Battery Cell Voltage #56',
    'k224219': 'Battery Cell Voltage #57',
    'k22421a': 'Battery Cell Voltage #58',
    'k22421b': 'Battery Cell Voltage #59',
    'k22421c': 'Battery Cell Voltage #60',
    'k22421d': 'Battery Cell Voltage #61',
    'k22421e': 'Battery Cell Voltage #62',
    'k22421f': 'Battery Cell Voltage #63',
    'k224220': 'Battery Cell Voltage #64',
    'k224221': 'Battery Cell Voltage #65',
    'k224222': 'Battery Cell Voltage #66',
    'k224223': 'Battery Cell Voltage #67',
    'k224224': 'Battery Cell Voltage #68',
    'k224225': 'Battery Cell Voltage #69',
    'k224226': 'Battery Cell Voltage #70',
    'k224227': 'Battery Cell Voltage #71',
    'k224228': 'Battery Cell Voltage #72',
    'k224229': 'Battery Cell Voltage #73',
    'k22422a': 'Battery Cell Voltage #74',
    'k22422b': 'Battery Cell Voltage #75',
    'k22422c': 'Battery Cell Voltage #76',
    'k22422d': 'Battery Cell Voltage #77',
    'k22422e': 'Battery Cell Voltage #78',
    'k22422f': 'Battery Cell Voltage #79',
    'k224230': 'Battery Cell Voltage #80',
    'k224231': 'Battery Cell Voltage #81',
    'k224232': 'Battery Cell Voltage #82',
    'k224233': 'Battery Cell Voltage #83',
    'k224234': 'Battery Cell Voltage #84',
    'k224235': 'Battery Cell Voltage #85',
    'k224236': 'Battery Cell Voltage #86',
    'k224237': 'Battery Cell Voltage #87',
    'k224238': 'Battery Cell Voltage #88',
    'k224239': 'Battery Cell Voltage #89',
    'k22423a': 'Battery Cell Voltage #90',
    'k22423b': 'Battery Cell Voltage #91',
    'k22423c': 'Battery Cell Voltage #92',
    'k22423d': 'Battery Cell Voltage #93',
    'k22423e': 'Battery Cell Voltage #94',
    'k22423f': 'Battery Cell Voltage #95',
    'k224240': 'Battery Cell Voltage #96',
    'ke16f08': 'Inst Kpower',
    'ke3ee8c': 'Inst W/kph',
    'ke3f60e': 'Inst W/mph',
    'kef253b': 'Charger AC Power',
    'ked22ae': 'Charger HV Power',
    'kea5b10': 'Last Charge AC KWh',

    # From default torque PID list
    'k10': 'Mass Air Flow Rate',
    'k11': 'Throttle Position(Manifold)',
    'k12': 'Air Status',
    'k14': 'Fuel trim bank 1 sensor 1',
    'k15': 'Fuel trim bank 1 sensor 2',
    'k16': 'Fuel trim bank 1 sensor 3',
    'k17': 'Fuel trim bank 1 sensor 4',
    'k18': 'Fuel trim bank 2 sensor 1',
    'k19': 'Fuel trim bank 2 sensor 2',
    'k1a': 'Fuel trim bank 2 sensor 3',
    'k1b': 'Fuel trim bank 2 sensor 4',
    'k1f': 'Run time since engine start',
    'k21': 'Distance traveled with MIL/CEL lit',
    'k22': 'Fuel Rail Pressure (relative to manifold vacuum)',
    'k23': 'Fuel Rail Pressure',
    'k24': 'O2 Sensor1 Equivalence Ratio',
    'k25': 'O2 Sensor2 Equivalence Ratio',
    'k26': 'O2 Sensor3 Equivalence Ratio',
    'k27': 'O2 Sensor4 Equivalence Ratio',
    'k28': 'O2 Sensor5 Equivalence Ratio',
    'k29': 'O2 Sensor6 Equivalence Ratio',
    'k2a': 'O2 Sensor7 Equivalence Ratio',
    'k2b': 'O2 Sensor8 Equivalence Ratio',
    'k2c': 'EGR Commanded',
    'k2d': 'EGR Error',
    'k2f': 'Fuel Level (From Engine ECU)',
    'k3': 'Fuel Status',
    'k31': 'Distance traveled since codes cleared',
    'k32': 'Evap System Vapor Pressure',
    'k33': 'Barometric pressure (from vehicle)',
    'k34': 'O2 Sensor1 Equivalence Ratio(alternate)',
    'k3c': 'Catalyst Temperature (Bank 1 Sensor 1)',
    'k3d': 'Catalyst Temperature (Bank 2 Sensor 1)',
    'k3e': 'Catalyst Temperature (Bank 1 Sensor 2)',
    'k3f': 'Catalyst Temperature (Bank 2 Sensor 2)',
    'k4': 'Engine Load',
    'k42': 'Voltage (Control Module)',
    'k43': 'Engine Load(Absolute)',
    'k44': 'Commanded Equivalence Ratio(lambda)',
    'k45': 'Relative Throttle Position',
    'k46': 'Ambient air temp',
    'k47': 'Absolute Throttle Position B',
    'k49': 'Accelerator PedalPosition D',
    'k4a': 'Accelerator PedalPosition E',
    'k4b': 'Accelerator PedalPosition F',
    'k5': 'Engine Coolant Temperature',
    'k52': 'Ethanol Fuel %',
    'k5a': 'Relative Accelerator Pedal Position',
    'k5c': 'Engine Oil Temperature',
    'k6': 'Fuel Trim Bank 1 Short Term',
    'k7': 'Fuel Trim Bank 1 Long Term',
    'k78': 'Exhaust Gas Temperature 1',
    'k79': 'Exhaust Gas Temperature 2',
    'k8': 'Fuel Trim Bank 2 Short Term',
    'k9': 'Fuel Trim Bank 2 Long Term',
    'ka': 'Fuel pressure',
    'kb': 'Intake Manifold Pressure',
    'kb4': 'Transmission Temperature(Method 2)',
    'kc': 'Engine RPM',
    'kd': 'Speed (OBD)',
    'ke': 'Timing Advance',
    'kf': 'Intake Air Temperature',
    'kfe1805': 'Transmission Temperature(Method 1)',
    'kff1001': 'Speed (GPS)',
    'kff1005': 'GPS Longitude',
    'kff1006': 'GPS Latitude',
    'kff1007': 'GPS Bearing',
    'kff1010': 'GPS Altitude',
    'kff1201': 'Miles Per Gallon(Instant)',
    'kff1202': 'Turbo Boost & Vacuum Gauge',
    'kff1203': 'Kilometers Per Liter(Instant)',
    'kff1204': 'Trip Distance',
    'kff1205': 'Trip average MPG',
    'kff1206': 'Trip average KPL',
    'kff1207': 'Liters Per 100 Kilometer(Instant)',
    'kff1208': 'Trip average Litres/100 KM',
    'kff120c': 'Trip distance (stored in vehicle profile)',
    'kff1214': 'O2 Volts Bank 1 sensor 1',
    'kff1215': 'O2 Volts Bank 1 sensor 2',
    'kff1216': 'O2 Volts Bank 1 sensor 3',
    'kff1217': 'O2 Volts Bank 1 sensor 4',
    'kff1218': 'O2 Volts Bank 2 sensor 1',
    'kff1219': 'O2 Volts Bank 2 sensor 2',
    'kff121a': 'O2 Volts Bank 2 sensor 3',
    'kff121b': 'O2 Volts Bank 2 sensor 4',
    'kff1220': 'Acceleration Sensor(X axis)',
    'kff1221': 'Acceleration Sensor(Y axis)',
    'kff1222': 'Acceleration Sensor(Z axis)',
    'kff1223': 'Acceleration Sensor(Total)',
    'kff1225': 'Torque',
    'kff1226': 'Horsepower (At the wheels)',
    'kff122d': '0-60mph Time',
    'kff122e': '0-100kph Time',
    'kff122f': '1/4 mile time',
    'kff1230': '1/8 mile time',
    'kff1237': 'GPS vs OBD Speed difference',
    'kff1238': 'Voltage (OBD Adapter)',
    'kff1239': 'GPS Accuracy',
    'kff123a': 'GPS Satellites',
    'kff123b': 'GPS Bearing',
    'kff1240': 'O2 Sensor1 wide-range Voltage',
    'kff1241': 'O2 Sensor2 wide-range Voltage',
    'kff1242': 'O2 Sensor3 wide-range Voltage',
    'kff1243': 'O2 Sensor4 wide-range Voltage',
    'kff1244': 'O2 Sensor5 wide-range Voltage',
    'kff1245': 'O2 Sensor6 wide-range Voltage',
    'kff1246': 'O2 Sensor7 wide-range Voltage',
    'kff1247': 'O2 Sensor8 wide-range Voltage',
    'kff1249': 'Air Fuel Ratio(Measured)',
    'kff124a': 'Tilt(x)',
    'kff124b': 'Tilt(y)',
    'kff124c': 'Tilt(z)',
    'kff124d': 'Air Fuel Ratio(Commanded)',
    'kff124f': '0-200kph Time',
    'kff1257': 'CO₂ in g/km (Instantaneous)',
    'kff1258': 'CO₂ in g/km (Average)',
    'kff125a': 'Fuel flow rate/minute',
    'kff125c': 'Fuel cost (trip)',
    'kff125d': 'Fuel flow rate/hour',
    'kff125e': '60-120mph Time',
    'kff125f': '60-80mph Time',
    'kff1260': '40-60mph Time',
    'kff1261': '80-100mph Time',
    'kff1263': 'Average trip speed(whilst moving only)',
    'kff1264': '100-0kph Time',
    'kff1265': '60-0mph Time',
    'kff1266': 'Trip Time(Since journey start)',
    'kff1267': 'Trip time(whilst stationary)',
    'kff1268': 'Trip Time(whilst moving)',
    'kff1269': 'Volumetric Efficiency (Calculated)',
    'kff126a': 'Distance to empty (Estimated)',
    'kff126b': 'Fuel Remaining (Calculated from vehicle profile)',
    'kff126d': 'Cost per mile/km (Instant)',
    'kff126e': 'Cost per mile/km (Trip)',
    'kff1270': 'Barometer (on Android device)',
    'kff1271': 'Fuel used (trip)',
    'kff1272': 'Average trip speed(whilst stopped or moving)',
    'kff1273': 'Engine kW (At the wheels)',
    'kff1275': '80-120kph Time',
    'kff1276': '60-130mph Time',
    'kff1277': '0-30mph Time',
    'kff5201': 'Miles Per Gallon(Long Term Average)',
    'kff5202': 'Kilometers Per Liter(Long Term Average)',
    'kff5203': 'Liters Per 100 Kilometer(Long Term Average)',
}

# Extra information about each ID
metadata = {}



# Load in config information
influx_conf = {}
with open('influx.conf') as f:
    for l in f:
        fields = l.split('=')
        if len(fields) == 2:
            influx_conf[fields[0].strip()] = fields[1].strip()

# Connect to the database
inf_client = influxdb.InfluxDBClient(influx_conf['host'],
                                     influx_conf['port'],
                                     influx_conf['user'],
                                     influx_conf['password'],
                                     influx_conf['database'])



class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Parse out the GET URL parameters
        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)

        # Create the structure we send to influx
        measurement = ''
        t = None
        fields = {}
        tags = {}

        # Parse for tags
        pyt = datetime.datetime.fromtimestamp(float(params['time'][0])/1000)
        t = arrow.get(pyt, 'US/Eastern')
        tags['version'] = int(params['v'][0])
        tags['device_id'] = params['id'][0]
        device_id = tags['device_id']

        # Make sure there is room for metadata
        if not device_id in metadata:
            metadata[device_id] = {}

        # Append additional tags
        for k,v in metadata[device_id].items():
            tags[k] = v

        # Check if this is a metadata message full of descriptions of the
        # PIDs.
        user_message = False
        for k,v in params.items():
            if k.startswith('userFullName'):
                user_message = True
                break

        # Check if this is just units
        unit_message = False
        if not user_message:
            for k,v in params.items():
                if k.startswith('defaultUnit'):
                    unit_message = True
                    break



        if user_message:
            # Try to use this to fill in anything we don't yet have.
            for k,v in params.items():
                if k.startswith('userFullName'):
                    pid = 'k' + k[12:]
                    fullname = v[0].strip()

                    # Check for weird symbols from the bolt ev PID list
                    if fullname[0] == '!' or fullname[0] == '*' \
                       or fullname[0] == '?' or fullname[0] == '+':
                       fullname = fullname[1:]



                    # Check to see if this is useful (i.e. we don't have
                    # this mapping already).
                    if not pid in MAPPINGS:
                        MAPPINGS[pid] = fullname


        elif unit_message:
            # Just want to skip this message
            pass


        elif 'notice' in params:
            # Handle a notification type message

            measurement = 'notification'
            fields['type'] = params['notice'][0]
            fields['class'] = params['noticeClass'][0]

        elif 'profileName' in params:
            # Just get the profile name
            metadata[device_id]['name'] = params['profileName'][0]

        else:
            # Handle a normal data packet
            measurement = 'torquepro'
            for k,v in params.items():
                if k == 'eml' or k == 'time' or k == 'session' or k == 'v' or k == 'id':
                    # ignore email address and other already used fields
                    continue
                elif v[0] == 'NaN':
                    # Skip invalid data. This is likely a divide by zero error.
                    continue
                elif v[0] == 'Infinity' or v[0] == '-Infinity':
                    # Skip invalid data. This is likely a divide by zero error.
                    continue
                else:
                    if k in MAPPINGS:
                        fields[MAPPINGS[k]] = float(v[0])
                    else:
                        fields[k] = float(v[0])


        print(t)
        print(fields)
        print(tags)

        # Only publish if we have a valid measurement
        if measurement != '':

            points = [
                {
                    'measurement': measurement,
                    "tags": tags,
                    "time": t.to('utc').isoformat(),
                    "fields": fields,
                }
            ]
            inf_client.write_points(points)


        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes('OK!', 'UTF-8'))


    def log_request(code='', size=''):
        pass

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))
