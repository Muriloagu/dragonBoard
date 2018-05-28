#!/usr/bin/env python
from dweet import Dweet
import spidev #lib
import time

from gpio_96boards import GPIO

TEMP = GPIO.gpio_id('GPIO_CS')

pins = (
    (TEMP, 'out'),
)

spi = spidev.SpiDev() #biblioteca SPI para acessar os pinos ADC1 e ADC2
spi.open(0,0) #acessando ADC2
spi.max_speed_hz = 10000
spi.mode = 0b00
spi.bits_per_word = 8

#cria o objeto de comunicacao com o portal dweet
dweet = Dweet()

#le a temperatudo no conectaor ADC2 e retorna o float
def readTemperature(gpio):

	r = spi.xfer2([0x01, 0xA0, 0x00])
	gpio.digital_write(TEMP, GPIO.HIGH)#liga o termometro
	adcout = (r[1] << 8) & 0b1100000000
	adcout = adcout | (r[2] & 0xff)	
	adc_temp = (adcout *5.0/1023-0.5)*100
	gpio.digital_write(TEMP, GPIO.LOW)	
	print ("Temperatura.:%2.1f" %adc_temp)
	
	return adc_temp

#envia a temperatura para o objeto na nuvem
def sendTemp(temperatura):

	dweet.dweet_by_name(name="iTemp", data={"temp":temperatura})
	#resposta = dweet.latest_dweet(name="iTemp")
	#print resposta['with'][0]['content']['temp']
	#print resposta


def run(gpio):

    while True:
	   sendTemp(readTemperature(gpio))
	   resposta = dweet.latest_dweet(name="iTemp")
           button_value_cloud = resposta['with'][0]['content']['temp']
	   print "Cloud Temp: %2.1f" %button_value_cloud
           time.sleep(5)
    
 
if __name__ == "__main__":

    
    with GPIO(pins) as gpio:
         run(gpio)

        
    

