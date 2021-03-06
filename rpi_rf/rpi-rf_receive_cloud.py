#!/usr/bin/env python3
#sudo pip3 install rpi-rf

import argparse
import signal
import sys,os
import time,datetime
import logging

from rpi_rf import RFDevice
from my_mqttClass import *      #Connect to your cloud if you have (second version)

rfdevice = None

pathname = os.path.join(os.getcwd(),'debug_rf.log') 
def logwrite(data):
    logging.info(data)          #存檔前先display, base on the level
    with open(pathname, 'w') as logstring:
        data = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+'===>'+data+'\n'
        #logstring.write(data.encode('utf-8'))
        logstring.write(data)

# pylint: disable=unused-argument
def exithandler(signal, frame):
    logwrite('You are break here!') #Ctrl+C 程序中止
    rfdevice.cleanup()
    sys.exit(0)

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )
#logger = logging.getLogger('test')

parser = argparse.ArgumentParser(description='Receives a decimal code via a 433/315MHz GPIO device')
parser.add_argument('-g', dest='gpio', type=int, default=27,
                    help="GPIO pin (Default: 27)")
args = parser.parse_args()

signal.signal(signal.SIGINT, exithandler)
rfdevice = RFDevice(args.gpio)
rfdevice.enable_rx()
timestamp = None
logging.info("Listening for codes on GPIO " + str(args.gpio))

time_out=0
water=[]        #空列表for Send to cloud
area_temp=[]    #空列表for Send to cloud
area_hum=[]     #空列表for Send to cloud
device_adc6=[]  #空列表for Send to cloud
device_adc7=[]  #空列表for Send to cloud
while True:
    if rfdevice.rx_code_timestamp != timestamp:
        timestamp = rfdevice.rx_code_timestamp
        '''
        logging.info(str(temp) +
                    " [pulselength " + str(rfdevice.rx_pulselength) +
                    ", BitLength " + str(rfdevice.rx_bitlength) +
                    ", protocol " + str(rfdevice.rx_proto) + "]")
        '''        
        logging.info(hex(rfdevice.rx_code) +
                     " [pulselength " + str(rfdevice.rx_pulselength) +
                     ", BitLength " + str(rfdevice.rx_bitlength) +
                     ", protocol " + str(rfdevice.rx_proto) + "]")

        temp = rfdevice.rx_code&0xfffe0000          #used 15bit for id &group
        if(temp==0x33300000) or (temp==0x33320000) or (temp==0x33340000) or (temp==0x33360000): #DS18b02 applications.
            if((rfdevice.rx_code&0x00010000) > 0):  #sign "-" for DS18b02 temperature sensor
                temp=0.0-(rfdevice.rx_code&0x0000ffff)/10
            else:
                temp=(rfdevice.rx_code&0x0000ffff)/10

            logging.info("DS18B02 Temperature is " + str(temp))  

            water.append(temp)
            if len(water)>=30:
                water.sort(reverse = True)          #降序
                temp=(water[15]+water[16])/2
                water=[]    #空列表
                try:
                    Fish=Fish_device()                  #Connect to your cloud if you have
                    Fish.publish("Temp",temp)           #發布--Temp
                    Fish.subscribe("Temp")              #訂閱
                except Exception as ex:
                    logwrite("An Error occurred: "+ str(ex))    #存檔例外原因

        elif(temp==0x33380000) or (temp==0x333a0000) or (temp==0x333c0000) or (temp==0x333e0000): #DHT22 applications
            if((rfdevice.rx_code&0x00010000) > 0):  #sign "-" for DHT22 temperature / Humidity
                temp=0.0-((rfdevice.rx_code&0x0000ff80) >> 7)/10
            else:
                temp=((rfdevice.rx_code&0x0000ff80) >> 7)/10
            
            logging.info("Temperature is " + str(temp))

            area_temp.append(temp)
            if len(area_temp)>=30:
                area_temp.sort(reverse = True)      #降序
                temp=(area_temp[15]+area_temp[16])/2
                area_temp=[]    #空列表
                try:
                    Office=Office_device()              #Connect to your cloud if you have
                    Office.publish("Temperature",temp)  #發布--Temperature
                    Office.subscribe("Temperature")     #訂閱
                except Exception as ex:
                    logwrite("An Error occurred: "+ str(ex))    #存檔例外原因

            temp=rfdevice.rx_code&0x0000007f
            logging.info("Humidity is " + str(temp) + "%RH")

            area_hum.append(temp)
            if len(area_hum)>=30:
                area_hum.sort(reverse = True)       #降序
                temp=(area_hum[15]+area_hum[16])/2
                area_hum=[]    #空列表
                try:
                    Office.publish("Humidity",temp)     #發布--Humidity
                    Office.subscribe("Humidity")        #訂閱
                except Exception as ex:
                    logwrite("An Error occurred: "+ str(ex))    #存檔例外原因
        
        elif(temp==0x33200000) or (temp==0x33220000) or (temp==0x33240000) or (temp==0x33280000): #ADC input applications
            temp=(rfdevice.rx_code&0x0001ff00) >> 8 #Arduino A6 input (got 9bit)
            logging.info("A6 (9bit) is "+ str(temp))   

            device_adc6.append(temp)
            if len(device_adc6)>=30:
                device_adc6.sort(reverse = True)    #降序
                temp=(device_adc6[15]+device_adc6[16])/2
                device_adc6=[]    #空列表
                try:
                    Fish=Fish_device()                  #Connect to your cloud if you have
                    Fish.publish("abc",temp)            #發布--氬硝酸
                    Fish.subscribe("abc")               #訂閱
                except Exception as ex:
                    logwrite("An Error occurred: "+ str(ex))    #存檔例外原因

            temp=rfdevice.rx_code&0x000000ff        #Arduino A7 input (got 8bit)
            logging.info("A7 (8bit) is "+ str(temp))

            device_adc7.append(temp)
            if len(device_adc7)>=30:
                device_adc7.sort(reverse = True)    #降序
                temp=(device_adc7[15]+device_adc7[16])/2
                device_adc7=[]    #空列表
                try:
                    Fish.publish("bc",temp)             #發布--氨氮
                    Fish.subscribe("bc")                #訂閱
                except Exception as ex:
                    logwrite("An Error occurred: "+ str(ex))    #存檔例外原因
        time_out=0
    else:
        time_out+=1
        if time_out>60000:  #0.01x60x10min
            time_out=0
            logwrite('Your time out(10 minutes)happen %s  %s'%(str(timestamp), str(rfdevice.rx_code_timestamp)))
    time.sleep(0.01)
logwrite('You are break loop!')
rfdevice.cleanup()
