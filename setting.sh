#!/bin/bash

if [ "$1" = "stop" ]
then /opt/excelfore/esync/start.sh stop

 

elif [ "$1" = "start" ]
then 

route add default gw 172.20.2.2

ping hao123.com -c 5

date -s "$(wget -qSO- www.qq.com 2>&1 | grep Date: | cut -d' ' -f5-8)"-8:00

rm -rf /otalog/*

rm -rf /run/media/mmcblk0p3/OTA/*

sleep 1

mkdir /otalog

mkdir -p /system/usr/lib/

scp /opt/demo/FOTA_API/libotahelper.so /system/usr/lib/

sleep 1

cd /system/usr/lib

mv libotahelper.so libota.so


/opt/excelfore/esync/start.sh start &

ps -ef | grep esync

sleep 2

echo 1 > /run/media/mmcblk0p3/OTA/misc/ota_events/set_eol
sleep 2

ps -ef | grep esync

sleep 2
tail -f /otalog/dmclient.log | grep -E "Response|xl4.sota-report"

else

echo please enter command with argument start or stop

fi
:<<!
sleep 5
!
