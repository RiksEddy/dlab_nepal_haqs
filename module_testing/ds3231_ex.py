import time
from ds3231 import ds3231

I2C_PORT = 0
I2C_SDA = 16
I2C_SCL = 17

rtc = ds3231(I2C_PORT,I2C_SCL,I2C_SDA)
rtc.set_time('13:28:00,Thursday,2023-08-17')
while True:
    timestamp = rtc.read_time()
    time.sleep(1)
    #rtc.set_alarm_time('13:45:55,Monday,2021-05-24')
