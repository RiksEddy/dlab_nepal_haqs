import time, machine
from pms5003 import PMS5003

print("""pms5003_test.py - Continously print all data values.
""")
"""
#brown board
UART_PORT = 1
PIN_ENABLE = 1
PIN_RESET = 0
UART_TX = 4
UART_RX = 5
"""
#green board
UART_PORT = 1
PIN_ENABLE = 7
PIN_RESET = 6
UART_TX = 8
UART_RX = 9

# Configure the PMS5003 for Enviro+
pms5003 = PMS5003(
    uart=machine.UART(UART_PORT, tx=machine.Pin(UART_TX), rx=machine.Pin(UART_RX), baudrate=9600),
    pin_enable=machine.Pin(PIN_ENABLE),
    pin_reset=machine.Pin(PIN_RESET),
    mode="active"
)

#added new command called pms5003.cmd_sleep() and pms5003.cmd_wakeup()

while True:
    data = pms5003.read() #reads only PM2.5 ug/m3
    print(data)
    pms5003.cmd_sleep()
    time.sleep(5.0)
    pms5003.cmd_wakeup()
    time.sleep(5.0)