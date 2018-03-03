import socket
import cv2
import json
import time
import base64

cli = socket.socket()
cli.connect(("127.0.0.1", 9876))
cap = cv2.VideoCapture(1)
while 1:
    ret, frame = cap.read()
    resized = cv2.resize(frame, (320, 240), interpolation=cv2.INTER_AREA)

    filename = "buf_img_dxp.jpg"
    cv2.imwrite(filename, resized)

    with open(filename, 'rb') as f:
        bin_payload = f.read()
    try:

        img = {"img": (base64.b64encode(bin_payload)).decode(), "id": "12767369"}
        # img = (base64.b64encode(bin_payload), "12767362")
        data=json.dumps(img)
        # print(data)
        # print(len(data))
        cli.sendall(data.encode())
        time.sleep(0.1)
    except Exception as e:
        print(e)
        break

