import serial
import datetime
import time
from sense_hat import SenseHat
import BlynkLib
 
BLYNK_AUTH = 'd0cbc51243284f1e8b1cdca4ba4f4c5f' 
blynk = BlynkLib.Blynk(BLYNK_AUTH)

port = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=2.0)

@blynk.VIRTUAL_READ(5)
def my_read_handler():
    # this widget will show some time in seconds..
    sense = SenseHat()
    temp = sense.get_temperature()
    blynk.virtual_write(5, temp) 
 
def read_pm_line(_port):
    rv = b''
    while True:
        ch1 = _port.read()
        if ch1 == b'\x42':
            ch2 = _port.read()
            if ch2 == b'\x4d':
                rv += ch1 + ch2
                rv += _port.read(40)
                return rv
 
blynk.run() 
while True:
    try:
        rcv = read_pm_line(port)
        res = {'timestamp': datetime.datetime.now(),
               'apm10': rcv[4] * 256 + rcv[5],
               'apm25': rcv[6] * 256 + rcv[7],
               'apm100': rcv[8] * 256 + rcv[9],
               'pm10': rcv[10] * 256 + rcv[11],
               'pm25': rcv[12] * 256 + rcv[13],
               'pm100': rcv[14] * 256 + rcv[15],
               'gt03um': rcv[16] * 256 + rcv[17],
               'gt05um': rcv[18] * 256 + rcv[19],
               'gt10um': rcv[20] * 256 + rcv[21],
               'gt25um': rcv[22] * 256 + rcv[23],
               'gt50um': rcv[24] * 256 + rcv[25],
               'gt100um': rcv[26] * 256 + rcv[27]
               }
        sense = SenseHat()
        sense.clear()
        pressure = sense.get_pressure()
        temp = sense.get_temperature()
        humidity = sense.get_humidity()
        print("temperature = ",temp)
        print("pressure = ",pressure)
        print("humidity = ",humidity)
        print('===============\n'
              'PM1.0(CF=1): {}\n'
              'PM2.5(CF=1): {}\n'
              'PM10 (CF=1): {}\n'
              'PM1.0 (STD): {}\n'
              'PM2.5 (STD): {}\n'
              'PM10  (STD): {}\n'
              '>0.3um     : {}\n'
              '>0.5um     : {}\n'
              '>1.0um     : {}\n'
              '>2.5um     : {}\n'
              '>5.0um     : {}\n'
              '>10um      : {}'.format(res['apm10'], res['apm25'], res['apm100'],
                                       res['pm10'], res['apm25'], res['pm100'],
                                       res['gt03um'], res['gt05um'], res['gt10um'],
                                       res['gt25um'], res['gt50um'], res['gt100um']))

    except KeyboardInterrupt:
        break