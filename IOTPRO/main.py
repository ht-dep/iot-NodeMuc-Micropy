# tcp clientwifi_address
#网关代码-nodeMcu

import socket
import utime
import dht
import machine
import gc
import utime
import ujson
import network
wifi_address="MERCURY_C0428A", ""


def getTH():
    p = machine.Pin(5)
    d = dht.DHT11(p)
    d.measure()
    #    while 1:
    t = d.temperature()
    h = d.humidity()
    print("当前温度："), t
    print("当前空气湿度："), h
    #        utime.sleep(5)
    gc.collect()
    return (t, h)


def server():
    addr = socket.getaddrinfo("192.168.1.101", 9876)[0][-1]
    print(addr)
    s = socket.socket()
    s.connect(addr)
    while 1:
        data = getTH()
        print("数据：", data, "  长度：", len(data))
        jdata = ujson.dumps(data)
        s.send(bytes(jdata, 'utf8'))
        utime.sleep(5)
        gc.collect()


def do_connect_hostspot():
    sta_if = network.WLAN(network.STA_IF)
    retry = 0
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(wifi_address)
        while not sta_if.isconnected():
            utime.sleep(1)
            retry = retry + 1
        print('network config:', sta_if.ifconfig())
    gc.collect()

def main():
    try:
        while 1:
            # machine.idle()
            try:
                do_connect_hostspot()
                server()
                utime.sleep(60)
                gc.collect()
            except Exception as e:
                print(e)
            finally:
                pass
    except Exception as e:
        print(e)
    finally:
        pass

main()
