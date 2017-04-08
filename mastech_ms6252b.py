from serial import *
from struct import unpack


try:
    anemometer = Serial(port=sys.argv[1],
                        baudrate=9600,
                        bytesize=EIGHTBITS,
                        parity=PARITY_NONE,
                        stopbits=STOPBITS_ONE,
                        timeout=None)
except SerialException as e:
    print e
    sys.exit(1)


while(1):
    raw_data = unpack(13 * 'c', anemometer.read(13))

    temperature_mode = ord(raw_data[0])
    temperature_unit = ord(raw_data[1])
    temperature = unpack('>H', raw_data[6] + raw_data[7])[0] / 10.0

    humidity = unpack('>H', raw_data[2] + raw_data[3])[0] / 10.0

    wind_mode_0 = ord(raw_data[8])
    wind_mode_1 = ord(raw_data[9])
    wind_mode_2 = ord(raw_data[12])
    wind_data = unpack('>H', raw_data[10] + raw_data[11])[0] / 100.0

    if temperature_mode == 0:
        if temperature_unit == 1:
            print 'Temperature', temperature, 'C'
        elif temperature_unit == 2:
            print 'Temperature', temperature, 'F'
    if temperature_mode == 1:
        if temperature_unit == 1:
            print 'Temperature DP', temperature, 'C'
        elif temperature_unit == 2:
            print 'Temperature DP', temperature, 'F'
    if temperature_mode == 2:
        if temperature_unit == 1:
            print 'Temperature WB', temperature, 'C'
        elif temperature_unit == 2:
            print 'Temperature WB', temperature, 'F'

    if wind_mode_0 == 1 and wind_mode_1 == 1 and wind_mode_2 == 3:
        print 'Wind Velocity', wind_data, 'm/s'
    elif wind_mode_0 == 1 and wind_mode_1 == 2 and wind_mode_2 == 3:
        print 'Wind Velocity', wind_data, 'km/s'
    elif wind_mode_0 == 1 and wind_mode_1 == 3 and wind_mode_2 == 3:
        print 'Wind Velocity', wind_data, 'mil/h'
    elif wind_mode_0 == 1 and wind_mode_1 == 4 and wind_mode_2 == 1:
        print 'Wind Velocity', wind_data, 'ft/m'
    elif wind_mode_0 == 1 and wind_mode_1 == 5 and wind_mode_2 == 3:
        print 'Wind Velocity', wind_data, 'ft/s'
    elif wind_mode_0 == 1 and wind_mode_1 == 6 and wind_mode_2 == 3:
        print 'Wind Velocity', wind_data, 'knots'
    elif wind_mode_0 == 2 and wind_mode_1 == 1 and wind_mode_2 == 3:
        print 'Wind Flow', wind_data, 'CMS'
    elif wind_mode_0 == 2 and wind_mode_1 == 2 and wind_mode_2 == 2:
        wind_data = wind_data * 10.0
        print 'Wind Flow', wind_data, 'CMM'
    elif wind_mode_0 == 2 and wind_mode_1 == 3 and wind_mode_2 == 2:
        wind_data = wind_data * 10.0
        print 'Wind Flow', wind_data, 'CFM'

    print 'Humidity', humidity, '%RH \n'
