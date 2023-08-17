import machine
import sdcard
import uos

"""
#brown board
SPI_PORT = 1
SPI_MISO = 8
SPI_CS = 9
SPI_SCK = 10
SPI_MOSI = 11
"""
#green board
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

with open("/sd/data.txt", "w") as file:
    print("Writing to data.txt...")
    file.write("date time temp(C) humidity(%) pressure(hPa) VOC(KOhms) pm2.5_std(ug/m3) pm2.5_env(ug/m3)\r\n")
  
with open("/sd/data.txt", "r") as file:
    print("Reading data.txt...")
    data = file.read()
    print(data)


