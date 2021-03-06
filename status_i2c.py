#!/usr/bin/env python
#coding=utf-8
# sudo apt-get install Adafruit_Python_SSD1306
# sudo apt-get install pillow
# sudo apt-get install python-imaging 
# sudo apt-get install python-smbus
#python status_spi.py
#python status_i2c.py

#import spidev as SPI
#import SSD1306
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import time
from PIL import Image, ImageDraw, ImageFont
import subprocess

# Raspberry Pi pin configuration: I2C
RST = None     # on the PiOLED this pin isnt used
DC = None
SPI_PORT = 0
SPI_DEVICE = 0
# 128x32 display with hardware I2C:
#disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)      #若硬體是128x64則字體變大
# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
# Note you can change the I2C address by passing an i2c_address parameter like:
#disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)
# Alternatively you can specify an explicit I2C bus number, for example
#disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_bus=2)


# Raspberry Pi pin configuration: SPI
#RST = 20
#DC = 16
#SPI_PORT = 0
#SPI_DEVICE = 1

# 128x32 display with hardware I2C:
#disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# 128x64 display with hardware I2C:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Note you can change the I2C address by passing an i2c_address parameter like:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

# Alternatively you can specify an explicit I2C bus number, for example
# with the 128x32 display you would use:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_bus=2)

# 128x32 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# 128x64 display with hardware SPI:
#disp = cp_SSD1306.SSD1306(RST, DC, SPI.SpiDev(SPI_PORT, SPI_DEVICE))
#disp = cp_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))
#disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# Alternatively you can specify a software SPI implementation by providing
# digital GPIO pin numbers for all the required display pins.  For example
# on a Raspberry Pi with the 128x32 display you might use:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, sclk=18, din=25, cs=22)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)

def fill_data_display():
    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True )
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell = True )
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True )
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell = True )

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    # Write two lines of text.
    draw.text((x, top),       "IP: " + str(IP),  font=font, fill=255)
    draw.text((x, top+16),     str(CPU), font=font, fill=255)
    draw.text((x, top+28),    str(MemUsage),  font=font, fill=255)
    draw.text((x, top+40),    str(Disk),  font=font, fill=255)
    draw.text((x, top+52),    str(__name__),  font=font, fill=255)
    # Display image.
    disp.image(image)
    disp.display()
#==========================================================================
if __name__ == "__main__":
    while True:
        fill_data_display()
        time.sleep(.2)