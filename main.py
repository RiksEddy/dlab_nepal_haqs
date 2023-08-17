from phew import logging, server, template
import uasyncio, os, time, uos
import network, machine
import _thread
import sdcard
from machine import Pin, I2C
from ds3231 import ds3231
from bme680 import *
from pms5003 import PMS5003

I2C_PORT = 0
I2C_SDA = 16
I2C_SCL = 17

rtc = ds3231(I2C_PORT,I2C_SCL,I2C_SDA)

logging.info('Configured RTC')

I2C_PORT = 1
I2C_SDA = 18
I2C_SCL = 19

i2c=I2C(I2C_PORT,sda=Pin(I2C_SDA), scl=Pin(I2C_SCL), freq=400000)

bme = BME680_I2C(i2c=i2c)

logging.info('Configured BME')

UART_PORT = 1
PIN_ENABLE = 7
PIN_RESET = 6
UART_TX = 8
UART_RX = 9

# Configure the PMS5003
pms5003 = PMS5003(
    uart=machine.UART(UART_PORT, tx=machine.Pin(UART_TX), rx=machine.Pin(UART_RX), baudrate=9600),
    pin_enable=machine.Pin(PIN_ENABLE),
    pin_reset=machine.Pin(PIN_RESET),
    mode="active"
)

logging.info('Configured PMS')

SPI_PORT = 1
SPI_MISO = 12
SPI_CS = 13
SPI_SCK = 14
SPI_MOSI = 15

CS = machine.Pin(SPI_CS, machine.Pin.OUT)
spi = machine.SPI(SPI_PORT,
                  baudrate=1000000,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(SPI_SCK),
                  mosi=machine.Pin(SPI_MOSI),
                  miso=machine.Pin(SPI_MISO))

for i in range(3):
    try: sd = sdcard.SDCard(spi,CS)
    except:
        if i<2: print("SD Not Detected")
        else: OSError("SD Card Error, Check Wiring and SD Card, Exiting!")
    else:
        print("SD Card Found!")
        break

vfs = uos.VfsFat(sd)
uos.mount(vfs, "/sd")

logging.info('Configured SD Card')

ssid = 'DLAB_Green_HAQ'       #Set access point name 
password = 'trashbag314!'      #Set your access point password

def connect():
    #Connect to AP
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password, channel=5)
    ap.active(True)
    while ap.active() == False:
        pass
    logging.info('WiFi AP Connection is successful')
    ip = ap.ifconfig()[0]
    channel = ap.config('channel')
    logging.info(f'Connected on channel: {channel}; ip: {ip}')
    return ip

ip = connect()

with open(f"/sd/server_data_720.txt", "w") as server_file:
    server_file.write("datetime temp(C) humidity(%) pressure(hPa) VOC(KOhms) pm2.5\r\n")
    for _ in range(720): server_file.write("X\n")

@server.route("/")
def index(request):
    return template.render_template(f"/sd/server_data_720.txt")

def data_collection(sampling_rate=300):
    averages = [0, 0.0, 0.0, 0, 0, 0]
    num_samples = 0
    while True:
        timestamp = rtc.read_time()
        readings = [int(bme.temperature), round(bme.humidity, 1), round(bme.pressure, 1), bme.gas]
        readings = readings + [max(0, int((int(pm25)-5)*3.51)) for pm25 in str(pms5003.read()).split()] #3.51 is 2-point calibrated value
        sample = f"{timestamp} " + "{} {} {} {} {} {}\n".format(*readings)
        averages = [readings[i] + averages[i] for i in range(6)]
        num_samples += 1
        logging.info('Data Collected')
        with open(f"/sd/data.txt", "a") as file:
            file.write(sample)
        logging.info('Data Stored')
        #update webserver with an hourly average of the measurements
        if num_samples == 12:
            averages = [round(reading_sum/12) for reading_sum in averages]
            with open(f"/sd/server_data_720.txt", "r+") as server_file:
                next(server_file) #skip header
                next(server_file) #skip oldest sample
                data = server_file.readlines()
            with open(f"/sd/server_data_720.txt", "w") as server_file:
                server_file.write("date time temp(C) humidity(%) pressure(hPa) VOC(KOhms) pm2.5_std(ug/m3) pm2.5_env(ug/m3)\r\n")
                for line in data: server_file.write(line)
                hourly_avg_sample = f"{timestamp} " + "{} {} {} {} {} {}\n".format(*averages)
                server_file.write(hourly_avg_sample)
            logging.info('Data Updated to Server')
            num_samples = 0
        pms5003.cmd_sleep()
        time.sleep(sampling_rate-5)
        pms5003.cmd_wakeup()
        time.sleep(5)
        
_thread.start_new_thread(data_collection, ())

if __name__ == '__main__':
    server.run()

