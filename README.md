## Application note


#### 1. How to setting "don't entry screen saving mode" in Desktop ? 
#### 因為Raspbian開機內定義有螢幕休眠, 所以我們需要rpi-rf_receive應用上取消休眠

sudo nano /etc/lightdm/lightdm.conf 
* [SeatDefaults]
* ...
* #xserver-command=X	    #Change to as below
* xserver-command=X -s 0 –dpms
* ...

#### 2. How to auto create CMD line to run application rpi-rf_receive in the X-windows mode
#### 視窗模式開機即開啟一個終端機模式, 並運行rpi-rf_receive (改用另一個)

sudo nano /etc/xdg/lxsession/LXDE-pi/autostart 
* ...
* #Exec = lxterminal -e /home/pi/autorun.sh    
* Exec = lxterminal -e "bash -c /home/pi/autorun.sh;bash"     
* ...

#### 3. Auto run application after log-in termainal in the X-Windows mode.
#### 視窗模式下自動開啟一個終端機模式(用戶登入或自動登入), 並運行應用程序

sudo nano /home/pi/.config/autostart/autoboot.desktop 
* ...
* [Desktop Entry]
* Type=Application
* Name=MyApplicationRun
* #Exec = lxterminal -e /home/pi/autorun.sh              #運行掛機 applivcation close aftern run 5day 
* Exec = lxterminal -e "bash -c /home/pi/autorun.sh;bash" #運行測試(Stay Bash)
* Icon=pictur.png
* ...
or

* [Desktop Entry]
* Encoding=UTF-8
* Type=Application
* Name=myprogram
* Exec=lxterminal -e bash -c '/home/pi/autorun.sh;$SHELL'     #bash run autorun.sh
* Terminal=true
* ...

>#The $SHELL makes the terminal stay open after myprogram ends its execution.


#### 4. autorun.sh 
#### 運行程序的內容

...

sudo python $jump_dir/status_spi.py &           #IP status display

sudo python3 $jump_dir/rpi_rf/rpi-rf_receive    #本程序main python


#### 5. Change receive code of the display on terminal dispaly.
#### 做了一些應用上的改變,改變接收代碼及顯示
##### 433MHz rf發送端已經定義的應用有DS18B02(temperature),DHT22(Temperature/Humidity),Arduino ADC

