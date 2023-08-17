from phew import logging, server, template
import uasyncio, os, time
import network

ssid = 'RPI_PICO_AP'       #Set access point name 
password = '12345678'      #Set your access point password

def connect():
    #Connect to AP
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password, channel=11)
    ap.active(True)
    while ap.active() == False:
        pass
    logging.info('Connection is successful')
    ip = ap.ifconfig()[0]
    print(ap.config('channel'))
    logging.info(f'Connected on {ip}')
    return ip

ip = connect()




@server.route("/")
def index(request):
    return template.render_template("data.csv")

server.run()
"""
loop = uasyncio.get_event_loop()

async def collect_data(print_val):
    while True:
        logging.info('measuring, storing data')
        await uasyncio.sleep(300)

async def main():
    server_task = server.run()
    await uasyncio.gather(collect_data(), server_task)

loop.run_until_complete(main())
"""

# while True:
#     web_server = server.run()
# # 
# web_server.close()
# 
# logging.info("After server run")

