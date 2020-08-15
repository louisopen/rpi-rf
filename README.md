## Application note


#### 1. How to setting "don't entry screen saving mode" in Desktop ? 
#### 因為Raspbian開機內定義有螢幕休眠, 所以我們需要rpi-rf_receive應用上取消休眠

sudo nano /etc/lightdm/lightdm.conf 
'
[SeatDefaults]
...
#xserver-command=X	#Change to as below
xserver-command=X -s 0 –dpms
...
'

#### 2. How to create a command line mode to run rpi-rf_receive in the X-windows mode? 
#### 視窗模式開機即開啟一個終端機模式, 並運行rpi-rf_receive (改用另一個)

sudo nano /etc/xdg/lxsession/LXDE-pi/autostart 
* * * 
...
#Exec = lxterminal -e /home/pi/autorun.sh                    
Exec = lxterminal -e "bash -c /home/pi/autorun.sh;bash"     
...
* * * 

#### 3. Auto run application after log-in.
#### 用戶自動登入時才運行程序的設置

sudo nano /home/pi/.config/autostart/autoboot.desktop 
* * * 
...
[Desktop Entry]
Type=Application
Name=MyApplicationRun
#Exec = lxterminal -e /home/pi/autorun.sh                    #運行掛機 applivcation close aftern run 5day 
Exec = lxterminal -e "bash -c /home/pi/autorun.sh;bash"     #運行測試(Stay Bash)
Icon=pictur.png
...
or

[Desktop Entry]
Encoding=UTF-8
Type=Application
Name=myprogram
Exec=lxterminal -e bash -c '/home/pi/autorun.sh;$SHELL'     #bash run autorun.sh
Terminal=true
...
* * *
#The $SHELL makes the terminal stay open after myprogram ends its execution.


#### 4. autorun.sh 
#### 運行程序的內容

...
sudo python $jump_dir/status_spi.py &           #IP status display
sudo python3 $jump_dir/rpi_rf/rpi-rf_receive    #本程序main python


#### 5. Change receive code of the display on terminal dispaly.
#### 做了一些應用上的改變,改變接收代碼及顯示
##### 433MHz rf發送端已經定義的應用有DS18B02(temperature),DHT22(Temperature/Humidity),Arduino ADC

...
...
        count+=1
        if count==30:
            count=0
            temp = rfdevice.rx_code&0xfffe0000          #used 15bit for id &group
            if(temp==0x33300000) or (temp==0x33320000) or (temp==0x33340000) or (temp==0x33360000): #DS18b02 applications.
                if((rfdevice.rx_code&0x00010000) > 0):  #sign "-" for DS18b02 temperature sensor
                    temp=0.0-(rfdevice.rx_code&0x0000ffff)/10
                else:
                    temp=(rfdevice.rx_code&0x0000ffff)/10          
                logging.info("DS18B02 Temperature is " + str(temp))
                my_sensor_temp("Temp",temp)             #send to cloud if you have the item

            elif(temp==0x33380000) or (temp==0x333a0000) or (temp==0x333c0000) or (temp==0x333e0000): #DHT22 applications
                if((rfdevice.rx_code&0x00010000) > 0):  #sign "-" for DHT22 temperature / Humidity
                    temp=0.0-((rfdevice.rx_code&0x0000ff80) >> 7)/10
                else:
                    temp=((rfdevice.rx_code&0x0000ff80) >> 7)/10
                logging.info("Temperature is " + str(temp)) 
                my_sensor_temp("Temperature",temp)      #send to cloud if you have the item

                temp=rfdevice.rx_code&0x0000007f
                logging.info("Humidity is " + str(temp) + "%RH")
                my_sensor_temp("Humidity",temp)         #send to cloud if you have the item

            elif(temp==0x33200000) or (temp==0x33220000) or (temp==0x33240000) or (temp==0x33280000): #ADC input applications
                temp=(rfdevice.rx_code&0x0001ff00) >> 8 #Arduino A6 input (got 9bit)
                logging.info("A6 (9bit) is "+ str(temp))   
                #my_sensor_temp("ADCvalue6",temp)       #send to cloud if you have the item

                temp=rfdevice.rx_code&0x000000ff        #Arduino A7 input (got 8bit)
                logging.info("A7 (8bit) is "+ str(temp))   
                my_sensor_temp("ADCvalue7",temp)        #send to cloud if you have the item

            else:
                pass
        else:
            pass
...

