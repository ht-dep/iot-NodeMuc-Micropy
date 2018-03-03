# tcp clientwifi_address
import socket
import utime
import dht
import machine
import gc
import utime
import ujson
import network
import esp
from machine import ADC

wifi_address = "MERCURY_C0428A", ""
sta_if = network.WLAN(network.STA_IF)

def get_FlashID():

    ID = esp.flash_id()
    gc.collect()
    return (ID,)

def get_Mac():
    s = sta_if.config('mac')
    mac = ('%02x-%02x-%02x-%02x-%02x-%02x') % (s[0], s[1], s[2], s[3], s[4], s[5])
    gc.collect()
    return (mac,)

def getTH():
    p = machine.Pin(14)
    d = dht.DHT22(p)
    d.measure()
    #    while 1:
    t = d.temperature()
    h = d.humidity()
    print("当前温度：", t)
    print("当前空气湿度：", h)
    #        utime.sleep(5)
    gc.collect()
    return (t, h)


def getAirDensity():
    adc = ADC(0)
    d = adc.read()
    print("当前空气浓度：", d)
    gc.collect()
    return (d,)


def server():
    FLASH_ID = get_FlashID()
    MAC_ID = get_Mac()
    # addr = socket.getaddrinfo("47.90.92.56", 59962)[0][-1]
    # addr = socket.getaddrinfo("192.168.199.72", 10001)[0][-1]
    addr = socket.getaddrinfo("120.79.34.76", 10001)[0][-1]
    print(addr)
    s = socket.socket()
    s.connect(addr)
    while 1:
        TW_data = getTH()  # 温湿度
        air_d = getAirDensity()

        data = TW_data + (MAC_ID,) + ("未知",) + (air_d,)
        print("数据：", data, "  长度：", len(data))
        jdata = ujson.dumps(data)
        s.send(bytes(jdata, 'utf8'))
        utime.sleep(5)
        gc.collect()


def do_connect_hostspot():
    # sta_if = network.WLAN(network.STA_IF)
    retry = 0
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect("squirrel", "rinpo301")
        while not sta_if.isconnected():
            utime.sleep(3)
            retry = retry + 1
        print('network config:', sta_if.ifconfig())
    gc.collect()


def main():
    try:
        while 1:
            # machine.idle()
            do_connect_hostspot()
            try:
                server()
                utime.sleep(30)
                gc.collect()
            except Exception as e:
                print("主逻辑流程异常:{}".format(e))
            finally:
                pass
    except Exception as e:
        print("网络连接异常：{}".format(e))
    finally:
        pass


main()
