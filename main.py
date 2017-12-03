import serial
import datetime
import time
from sense_hat import SenseHat
 
port = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=2.0)
 
 
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
        # print('0 start char1: dec= ', rcv[0],'hex=',format(rcv[0],'02x'))
        # print('1 start char2: dec= ', rcv[1],'hex=',format(rcv[1],'02x'))
        # print('2 frame len high8: dec= ', rcv[2],'hex=',format(rcv[2],'02x'))
        # print('3 frame len low8: dec= ', rcv[3],'hex=',format(rcv[3],'02x'))
        # print('4 data1 high8: dec= ', rcv[4],'hex=',format(rcv[4],'02x'))
        # print('5 data1 low8: dec= ', rcv[5],'hex=',format(rcv[5],'02x'))
        # print('6 data2 high8 dec= ', rcv[6],'hex=',format(rcv[6],'02x'))
        # print('7 dec= ', rcv[7],'hex=',format(rcv[7],'02x'))
        # print('8 data3 high8 dec= ', rcv[8],'hex=',format(rcv[8],'02x'))
        # print('9 dec= ', rcv[9],'hex=',format(rcv[9],'02x'))
        # print('10 data4 high8 dec= ', rcv[10],'hex=',format(rcv[10],'02x'))
        # print('11 dec= ', rcv[11],'hex=',format(rcv[11],'02x'))
        # print('12 data5 high8 dec= ', rcv[12],'hex=',format(rcv[12],'02x'))
        # print('13 dec= ', rcv[13],'hex=',format(rcv[13],'02x'))
        # print('14 data6 high8 dec= ', rcv[14],'hex=',format(rcv[14],'02x'))
        # print('15 dec= ', rcv[15],'hex=',format(rcv[15],'02x'))
        # print('16 data7 high8 dec= ', rcv[16],'hex=',format(rcv[16],'02x'))
        # print('17 dec= ', rcv[17],'hex=',format(rcv[17],'02x'))
        # print('18 data8 high8 dec= ', rcv[18],'hex=',format(rcv[18],'02x'))
        # print('19 dec= ', rcv[19],'hex=',format(rcv[19],'02x'))
        # print('20 data9 high8 dec= ', rcv[20],'hex=',format(rcv[20],'02x'))
        # print('21 dec= ', rcv[21],'hex=',format(rcv[21],'02x'))
        # print('22 data10 high8 dec= ', rcv[22],'hex=',format(rcv[22],'02x'))
        # print('23 dec= ', rcv[23],'hex=',format(rcv[23],'02x'))
        # print('24 data11 high8 dec= ', rcv[24],'hex=',format(rcv[24],'02x'))
        # print('25 dec= ', rcv[25],'hex=',format(rcv[25],'02x'))
        # print('26 data12 high8 dec= ', rcv[26],'hex=',format(rcv[26],'02x'))
        # print('27 dec= ', rcv[27],'hex=',format(rcv[27],'02x'))
        # print('28 data13 high8 dec= ', rcv[28],'hex=',format(rcv[28],'02x'))
        # print('29 dec= ', rcv[29],'hex=',format(rcv[29],'02x'))
        # print('30 Check high dec= ', rcv[30],'hex=',format(rcv[30],'02x'))
        # print('31 dec= ', rcv[31],'hex=',format(rcv[31],'02x'))
        # print('32 dec= ', rcv[32],'hex=',format(rcv[32],'02x'))
        # print('33 dec= ', rcv[33],'hex=',format(rcv[33],'02x'))
        # print('34 dec= ', rcv[34],'hex=',format(rcv[34],'02x'))
        # print('35 dec= ', rcv[35],'hex=',format(rcv[35],'02x'))
        # print('checksum_in = ', rcv[30]*256+rcv[31])
        # print('checksum = ', rcv[0]+rcv[1]+rcv[5]+rcv[7]+rcv[9]+rcv[11]+rcv[13]+rcv[15]+rcv[17]+rcv[19]+rcv[21]+rcv[23]+rcv[25]+rcv[27]+rcv[29])
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
        time.sleep(1)
    except KeyboardInterrupt:
        break