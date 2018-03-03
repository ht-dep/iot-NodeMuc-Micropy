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
import ssd1306

address = "WuHan"
wifi = "squirrel"
wifi_address = "rinpo301", ""
sta_if = network.WLAN(network.STA_IF)
i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(0), freq=100000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
oled.poweron()
oled.init_display()
count = 0


def general_display():
    global oled
    global count
    count = count + 1
    oled.text('WIFI:' + wifi, 1, 1)
    wlan = network.WLAN(network.STA_IF)
    ipconfig = wlan.ifconfig()
    # oled.text('I:'+ipconfig[0],1,8)
    # oled.text('pwd:123456',0,36)
    host = ipconfig[2]
    # oled.text('H:'+host, 0, 54)
    gc.collect()


def get_FlashID():
    gc.collect()
    ID = esp.flash_id()
    return (ID,)


def get_Mac():
    s = sta_if.config('mac')
    mac = ('%02x-%02x-%02x-%02x-%02x-%02x') % (s[0], s[1], s[2], s[3], s[4], s[5])
    gc.collect()
    return (mac,)

def getTH():
    p = machine.Pin(5)
    d = dht.DHT11(p)
    d.measure()
    #    while 1:
    t = d.temperature()
    h = d.humidity()
    print("当前温度：", t)
    print("当前空气湿度：", h)
    oled.fill(0)
    general_display()
    oled.text('Temp(C):' + str(t), 1, 24)
    oled.text('Hum(%):' + str(h), 1, 36)
    oled.show()
    #        utime.sleep(5)
    gc.collect()
    return (t, h)


def server():
    FLASH_ID = get_FlashID()
    MAC_ID=get_Mac()
    # addr = socket.getaddrinfo("47.90.92.56", 59962)[0][-1]
    # addr = socket.getaddrinfo("192.168.1.107", 9876)[0][-1]
    addr = socket.getaddrinfo("192.168.199.72", 10001)[0][-1]
    print(addr)
    s = socket.socket()
    s.connect(addr)
    while 1:
        TW_data = getTH()  # 温湿度
        data = TW_data + (MAC_ID,)
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
        # sta_if.connect("squirrel", "rinpo301")
        sta_if.connect("MERCURY_C0428A", "")
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


def record():
    l = ["Without you?", "I'd be a soul without a purpose."
                         "Without you?", "I'd be an emotion without a heart",
         "I'm a face without expression,A heart with no beat.",
         "Without you by my side,I'm just a flame without the"]

    import utime
    import ssd1306
    import machine
    i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(0), freq=100000)
    oled = ssd1306.SSD1306_I2C(128, 32, i2c)
    oled.poweron()
    a = ["i miss u ", "i'm very sad", "those days", "jing ", ]

    while 1:
        n = 0
        for i in a:
            oled.text(i, 1, n)
            n = n + 9
            oled.show()
            utime.sleep(5)
        oled.fill(0)
        utime.sleep(10)


if __name__ == "__main__":
    main()
