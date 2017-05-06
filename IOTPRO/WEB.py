from config import LOG
from flask import Flask, render_template, send_file

app = Flask(__name__)
logger = LOG.web()
import os
os.system("title WEB---FLASK服务")#修改命令行的显示标题
@app.route('/', methods=['GET', 'POST'])
def root():
    return send_file("page_front.html")

if __name__ == '__main__':
    app.run(port=8888)
