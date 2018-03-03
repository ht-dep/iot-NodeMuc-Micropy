from config import LOG
import json
from flask import Flask, render_template, send_file, request

app = Flask(__name__)
logger = LOG.web()
import os

# os.system("title WEB---FLASK服务")  # 修改命令行的显示标题

data = {"root": [
    {'name': 'ht1', 'age': 1, 'company': 'c1', 'price': 'p1', 'change1': '1', 'change': '1%', 'lastupdate': '11'},
    {'name': 'ht2', 'age': 2, 'company': 'c2', 'price': 'p2', 'change1': '2', 'change': '2%', 'lastupdate': '12'},
    {'name': 'ht3', 'age': 3, 'company': 'c3', 'price': 'p3', 'change1': '3', 'change': '3%', 'lastupdate': '13'},
]}

combox_data = {"root": [
    {'name': 'ht1', 'abbr': 1, 'company': 'c1', 'price': 'p1', 'change1': '1', 'change': '1%', 'lastupdate': '11'},
    {'name': 'ht2', 'abbr': 2, 'company': 'c2', 'price': 'p2', 'change1': '2', 'change': '2%', 'lastupdate': '12'},
    {'name': 'ht3', 'abbr': 3, 'company': 'c3', 'price': 'p3', 'change1': '3', 'change': '3%', 'lastupdate': '13'},
]}

many_data = {
    "rows": [
        {"bm": "1",
         "bm2": "1",
         "id": "11",
         "childrens": [
             {'bm': '1-1', 'bm2': '1-1', 'id': '1-11'},
             {'bm': '1-2', 'bm2': '1-2', 'id': '1-21'},
             {'bm': '1-3', 'bm2': '1-3', 'id': '1-31'},
         ]
         },
        {"bm": "2",
         "bm2": "2",
         "id": "22",
         "childrens": [
             {'bm': '2-1', 'bm2': '2-1', 'id': '2-12'},
             {'bm': '2-2', 'bm2': '2-2', 'id': '2-22'},
             {'bm': '2-3', 'bm2': '2-3', 'id': '2-32'},
         ]
         },
        {"bm": "3",
         "bm2": "3",
         "id": "33",
         "childrens": [
             {'bm': '3-1', 'bm2': '3-1', 'id': '3-13'},
             {'bm': '3-2', 'bm2': '3-2', 'id': '3-23'},
             {'bm': '3-3', 'bm2': '3-3', 'id': '3-33'},
         ]
         },
    ]
}

tree_data = {"rows":
    [
        {'text': "detention", 'leaf': True},
        {
            'text': "homework", 'expanded': False, 'children': [
            {'text': "book report", 'leaf': True},
            {'text': "alegrbra", 'leaf': True}
        ]
        },
        {'text': "buy lottery tickets", 'leaf': True}
    ]
}


# @app.route('/', methods=['GET', 'POST'])
# def root():
#     print("接收到请求")
#     print(request.method)
#     data = request.form.get("a")
#     print(data)
#     return "hello ext"

# return send_file("old.html")


@app.route('/store', methods=['GET', 'POST'])
def store():
    json_data = json.dumps(data)
    return json_data


@app.route('/tree', methods=['GET', 'POST'])
def tree():
    # json_data = json.dumps(combox_data)
    json_data = json.dumps(tree_data)
    return json_data


@app.route('/combox', methods=['GET', 'POST'])
def combox():
    # json_data = json.dumps(combox_data)
    json_data = json.dumps(many_data)
    return json_data


@app.route('/', methods=['GET', 'POST'])
def index():
    return send_file("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10003, threaded=True, debug=True)
