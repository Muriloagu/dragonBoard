import spidev
import time
from libsoc import gpio
from gpio_96boards import GPIO
from dweet import Dweet

VOLUME = GPIO.gpio_id('GPIO_CS') #SENSOR VOLUME DAGUA
TEMPERATURA = GPIO.gpio_id('GPIO_CS') #SENSOR DE TEMPERATURA
SOL = GPIO.gpio_id('GPIO_CS') #SENSOR DE LUMINOSIDADE
HUMIDADE = GPIO.gpio_id('GPIO_CS') #SENSOR DE HUMIDADE

ILUMINACAO = GPIO.gpio_id('GPIO_C') #LED
IRRIGACAO = GPIO.gpio_id('GPIO_B') #RELE - LIGADO A VALVULA SOLENOIDE

pins = ((VOLUME, 'out'),(TEMPERATURA, 'out'),(SOL, 'out'), (IRRIGACAO, 'out'), (ILUMINACAO, 'out'),(HUMIDADE, 'out'),)

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 10000
spi.mode = 0b00
spi.bits_per_word = 8


dweet = Dweet()

def readDigital(gpio):
	digital = [0,0]
	digital[0] = gpio.digital_read(ILUMINACAO)
	digital[1] = gpio.digital_read(IRRIGACAO)

	return digital

def writeDigital(gpio, digital):
	write = digital
	gpio.digital_write(ILUMINACAO, write[0])
	gpio.digital_write(IRRIGACAO, write[1])

	return digital

def readVol(gpio):

	gpio.digital_write(VOLUME, GPIO.HIGH)
	time.sleep(0.0002)
	gpio.digital_write(VOLUME, GPIO.LOW)
	r = spi.xfer2([0x01, (8+3)<<4, 0x00])#ADC3
	gpio.digital_write(VOLUME, GPIO.HIGH)

	adcout = (r[1] << 8) & 0b1100000000
	adcout3 = adcout | (r[2] & 0xff)

	return adcout3

def readHum(gpio):

	gpio.digital_write(HUMIDADE, GPIO.HIGH)
	time.sleep(0.0002)
	gpio.digital_write(HUMIDADE, GPIO.LOW)
	r = spi.xfer2([0x01, (8+1)<<4, 0x00])#ADC1
	gpio.digital_write(HUMIDADE, GPIO.HIGH)

	adcout = (r[1] << 8) & 0b1100000000
	adcout3 = adcout | (r[2] & 0xff)

	return adcout3

def readTemp(gpio):

	gpio.digital_write(TEMPERATURA, GPIO.HIGH)
	time.sleep(0.0002)
	gpio.digital_write(TEMPERATURA, GPIO.LOW)
	r = spi.xfer2([0x01, (8+0)<<4, 0x00]) #ADC0
	gpio.digital_write(TEMPERATURA, GPIO.HIGH)

	adcout = (r[1] << 8) & 0b1100000000
	adcout = adcout | (r[2] & 0xff)
	adc_temp = (adcout *5.0/1023-0.5)*100

	return adc_temp

def readLumi(gpio):

	gpio.digital_write(SOL, GPIO.HIGH)
	time.sleep(0.0002)
	gpio.digital_write(SOL, GPIO.LOW)
	r = spi.xfer2([0x01, (8+2)<<4, 0x00])#ADC2
	gpio.digital_write(SOL, GPIO.HIGH)

	adcout = (r[1] << 8) & 0b1100000000
	adcout2 = adcout | (r[2] & 0xff)

	#print("Luminosidade: %d" %adcout)
	return  adcout2

#def readDweet():

if __name__=='__main__':
	with GPIO(pins) as gpio:
		while True:
			digital = [0,0]
			resposta = dweet.latest_dweet(name="murilo_inatel")
			digital[0] =  resposta['with'][0]['content']['iluminacao']
			digital[1] =  resposta['with'][0]['content']['irrigacao']
			# era aqui writeDigital(gpio, digital)
			
			sol = readLumi(gpio)
			vol = readVol(gpio)
			hum = readHum(gpio)
			writeDigital(gpio, digital)
			#digital = readDigital(gpio)
			temp = readTemp(gpio)

			print "\n\nLEITURA: Sistema iRRigacao\nTemperatura: %2.1f\nSol: %d\nIluminacao: %d\nIrrigacao: %d\nVolume Dagua:%d\nHumidade do Ar:%d" %(temp,sol,digital[0], digital[1],vol,hum)

			dweet.dweet_by_name(name="murilo_inatel", data={"iluminacao":digital[0],"irrigacao": digital[1], "temperatura":temp, "sol": sol,"volume":vol, "humidade":hum})

			time.sleep(5)
