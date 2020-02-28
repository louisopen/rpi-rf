##### Application note
1. How to setting "don't entry screen saving mode" in Desktop ? 
因為Raspbian開機內定義有螢幕休眠, 所以我們需要rpi-rf_receive應用上取消休眠

update/edit the /etc/lightdm/lightdm.conf 

...
[SeatDefaults]
...
#xserver-command=X	#Change to as below
xserver-command=X -s 0 –dpms
...


2. How to create a command line mode to run rpi-rf_receive in the mode? 
開機即開啟終端機模式, 並運行rpi-rf_receove, 這樣開機後可以直接準備就緒

update/edit the /etc/xdg/lxsession/LXDE-pi/autostart 

...
Exec = lxterminal -e /home/pi/autorun.sh
...


3. Auto run application at log-in.
用戶登入時才運行程序的設置

pdate/edit the /home/pi/.config/autostart/autoboot.desktop 

[Desktop Entry]
Type=Application
Name=MyApplicationRun
Exec = lxterminal -e /home/pi/autorun.sh
Icon=pictur.png
...
or

[Desktop Entry]
Encoding=UTF-8
Type=Application
Name=myprogram
Exec=lxterminal -e bash -c '/home/pi/autorun.sh;$SHELL'
Terminal=true
...

#The $SHELL makes the terminal stay open after myprogram ends its execution.


4. autorun.sh 
運行程序的內容

...
sudo python $jump_dir/status_spi.py &           #IP display
sudo python3 $jump_dir/rpi_rf/rpi-rf_receive    #本程序main python


5. Change receive code of the display on terminal dispaly.
我們做了一些應用上的改變接收代碼及顯示(rf發送端已經定義了溫度單位及意義)

...
        if((rfdevice.rx_code&0xfffe0000) == 0x33340000):    #ID ok
            if((rfdevice.rx_code&0x00010000) > 0):  #sign "-"
                temp=0.0-(rfdevice.rx_code&0x0000ffff)/10
            else:
                temp=(rfdevice.rx_code&0x0000ffff)/10
            logging.info(str(temp))
            '''
            ...
            '''
...

