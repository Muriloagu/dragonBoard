import spidev
import time
from libsoc import gpio

from gpio_96boards import GPIO

POTENCIOMETRO = GPIO.gpio_id('GPIO_CS') #analogica ADC1
LED = GPIO.gpio_id('GPIO_A') #Porta Digital

pins = ((POTENCIOMETRO, 'out'),(LED, 'out'),)

spi = spidev.SpiDev() #biblioteca SPI para acessar os pinos ADC1 e ADC2
spi.open(0,0) #acessando ADC2
spi.max_speed_hz = 10000
spi.mode = 0b00
spi.bits_per_word = 8

def readPotenciometro(gpio):

	r = spi.xfer2([0x01, 0xA0, 0x00])
	gpio.digital_write(POTENCIOMETRO, GPIO.HIGH)#liga o potenciometro
	adcout = (r[1] << 8) & 0b1100000000
	adcout = adcout | (r[2] & 0xff)		
	print ("Valor do Pot.:%d" %adcout)
	return adcout
	
while True:
	with GPIO(pins) as gpio:
		value = readPotenciometro(gpio)
		if value > 500:
			gpio.digital_write(LED, GPIO.HIGH)
		else:
			gpio.digital_write(LED, GPIO.LOW)		

		time.sleep(0.5)




	
