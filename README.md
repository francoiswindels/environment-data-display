# Shows UV index from ARPANSA and pollution levels from woolloongabba station  
runs on raspberry pi 3B+ with an Adfruit Bonnet and RGB LED matrix  
https://learn.adafruit.com/adafruit-rgb-matrix-bonnet-for-raspberry-pi/  

RPI rgb led matrix library https://github.com/hzeller/rpi-rgb-led-matrix  

driving RGB matrices with RPI, adafruit bonnet and python script  
https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/driving-matrices  

air quality data and UV index are color coded based on safety recommendation from their respective agency  
Green: no concern  
Orange: moderate risk, mitigation recoemnded (UV:sunscreen, pollution: limit exercise if prolonged exposure )  
Red: take preventative action (avoid exposure)  

## /etc/rc.local
was modified to launch the script below  
i added sh /home/francois/airQualScript.sh & before exit 0  

## airQualScript.sh script 
below is executed every 10 minutes  
all python programmes are automatically killed (easy cleanup of rgb led matrix)  

#!/bin/sh  
while true  
do  
python /home/francois/rpi-rgb-led-matrix/bindings/python/samples/display_air_data_V2.py --led-cols=64 --led-brightness=50 &  
python /home/francois/safe_shutdown.py &  
sleep 10m  
sudo killall python  
sleep 5s  
done  

## added a shutdown button using
https://learn.sparkfun.com/tutorials/raspberry-pi-safe-reboot-and-shutdown-button

## This is the final box
![IMG20240122131654](https://github.com/francoiswindels/environment-data-display/assets/29170386/b906cf6f-3bbf-4127-a8b8-c3e1e8b79806)


first line is the UV index
line 2 & 3 are NO and CO in ppm
line 4 is PM10 in micro gram/m3

### air quality data are coming from
https://apps.des.qld.gov.au/air-quality/stations/?station=woo

### UV index data from ARPANSA
https://www.arpansa.gov.au/our-services/monitoring/ultraviolet-radiation-monitoring/ultraviolet-radiation-index



