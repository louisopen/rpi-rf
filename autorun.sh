#!/bin/bash
#This bash called by autoboot.desktop or rootcron   #autoboot.desktop存放到/home/pi/.config/autostart/
#chmod =777 autoboot.desktop
#sudo nano .bashrc   	#最後行添加 sh autorun.sh  同時(近端/遠端)啟動
#
#tr -d "\r" < autorun.sh > newname.sh    #if you can't cd to .... just do this command. #置入新系統時若發生此訊息
#tr -d "\r" < autorun.sh > newname.sh    #if you got ...Syntax error: end of file unexpected (expecting "then")

_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi

#su pi
source_dir=$PWD
jump_dir=/home/pi
cd $jump_dir

sudo python $jump_dir/status_spi.py &
#sudo python $jump_dir/status_i2c.py &

#sudo python3 $jump_dir/rpi_rf/rpi-rf_receive &
#sudo python3 $jump_dir/rpi_rf/rpi-rf_receive
sudo python3 $jump_dir/rpi_rf/rpi-rf_receive_cloud.py

cd $source_dir
exit 0