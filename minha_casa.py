import spidev
import time
from libsoc import gpio
from gpio_96boards import GPIO
from dweet import Dweet

TEMP = GPIO.gpio_id('GPIO_CS')
RELE = GPIO.gpio_id('GPIO_A')
LED = GPIO.gpio_id('GPIO_C')

pins = ((TEMP, 'out'), (RELE, 'out'), (LED, 'out'),)

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 10000
spi.mode = 0b00
spi.bits_per_word = 8

dweet = Dweet()


def readDigital(gpio):
	dados = [0,0]
	dados[0] = gpio.digital_read(LED)
	dados[1] = gpio.digital_read(RELE)

	return digital

def writeDigital(gpio, dados):
	escreve = dados
	gpio.digital_write(LED, escreve[0])
	gpio.digital_write(RELE, escreve[1])

	return escreve

def readTemp(gpio):

	gpio.digital_write(TEMP, GPIO.HIGH)
	time.sleep(0.0002)
	gpio.digital_write(TEMP, GPIO.LOW)
	r = spi.xfer2([0x01, 0xA0, 0x00])
	gpio.digital_write(TEMP, GPIO.HIGH)

	adcout = (r[1] << 8) & 0b1100000000
	adcout = adcout | (r[2] & 0xff)
	adc_temp = (adcout *5.0/1023-0.5)*100

	return adc_temp

if __name__=='__main__':
	with GPIO(pins) as gpio:
		while True:
			dados = [0,0]
			resposta = dweet.latest_dweet(name="minhacasa")
	        dados[0] =  resposta['with'][0]['content']['led']
	        dados[1] =  resposta['with'][0]['content']['rele']
			writeDigital(gpio, digital)
			temp = readTemp(gpio)
			digital = readDigital(gpio)
			print "Monitoramento Residencial\n"
			print "Temp: %2.1f\n led: %d\nrele: %d" %(temp, digital[0], digital[1])
			print "Registrando na Nuvem\n"
			dweet.dweet_by_name(name="minhacasa", data={"led":digital[0],"rele": digital[1], "Temperatura":temp})

			time.sleep(30)
