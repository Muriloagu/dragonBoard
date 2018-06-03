import spidev
import time
from libsoc import gpio

from gpio_96boards import GPIO

GPIO_CS = GPIO.gpio_id('GPIO_CS')

pins = ((GPIO_CS, 'out'),)

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 10000
spi.mode = 0b00
spi.bits_per_word = 8

def readTemparature(gpio):

	gpio.digital_write(GPIO_CS, GPIO.HIGH)
	time.sleep(0.0002)
	gpio.digital_write(GPIO_CS, GPIO.LOW)
	r = spi.xfer2([0x01, 0xA0, 0x00])
	gpio.digital_write(GPIO_A, GPIO.HIGH)
	adcout = (r[1] << 8) & 0b1100000000
	adcout = adcout | (r[2] & 0xff)

	adc_temp = (adcout *5.0/1023-0.5)*100

	return adc_temp



while True:
	with GPIO(pins) as gpio:
		temperatura = readTemparature(gpio)
		Ambiente = "Quarto" #aplicacao secundaria para capturar o ambiente
		print ("Temperatura no %s : %2.1f" %temperatura %Ambiente)
		if temperatura > 32:
			print("Sair deste ambiente e ligar climatização: %s" %Ambiente)
		else:
			print("Ambiente Liberado: %s" %Ambiente)

		time.sleep(0.5)
