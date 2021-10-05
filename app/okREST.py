from flask import Flask, request
from flask.templating import render_template
from base64 import b64decode, b64encode

import json
import requests

app = Flask(__name__)

@app.route('/www/<name>')
def helloName(name):
    return render_template('hellos.html', name=name)

@app.route('/file/encrypt', methods=['POST'])
def fileEncrypt():
    import okService
    data = request.get_json(force=True)
    body = data['body'].encode('utf-8')
    key1 = b64decode("othk6WkHQ4O6Iz//KZWpaM2fLXLQw80rD8Bt/XLtSuo=".encode('utf-8'))
    iv = b64decode("XYsr8+TbMFcCd9DHiCZGzg==".encode('utf-8'))
    key2 = b64decode("fbYeFx+06LRa47rZZH3Db6xO0rezOIitQ27r07ZEpbw=".encode('utf-8'))
    body1, body2 = okService.twoChannelEncrytion(key1, key2, iv, body)
    # key1, key2, iv, body1, body2 = okService.twoChannelEncrytion(body)
    # return { 'key1': b64encode(key1).decode('utf-8'), 'key2': b64encode(key2).decode('utf-8'), 'seed': b64encode(iv).decode('utf-8'), 'body1': b64encode(body1).decode('utf-8'), 'body2': b64encode(body2).decode('utf-8') }
    okService.twoChannelStore(b64encode(body1).decode('utf-8'), b64encode(body2).decode('utf-8'))
    return { 'key1': b64encode(key1).decode('utf-8'), 'key2': b64encode(key2).decode('utf-8'), 'seed': b64encode(iv).decode('utf-8') }

@app.route('/file/decrypt', methods=['POST'])
def fileDecrypt():
    import okService
    data = request.get_json(force=True)
    key1 = b64decode(data['key1'].encode('utf-8'))
    key2 = b64decode(data['key2'].encode('utf-8'))
    iv = b64decode(data['seed'].encode('utf-8'))
    body1, body2 = okService.twoChannelLoad("sCDC0109267107", "secM0803220193")
    body1 = b64decode(data['body1'].encode('utf-8'))
    body2 = b64decode(data['body2'].encode('utf-8'))
    body = okService.twoChannelDecrytion(key1, key2, iv, body1, body2)
    return { 'result': body.decode('utf-8').replace('\u0000', '') }


@app.route('/pAgent/register', methods=['POST'])
def register():
    data = request.get_json(force=True)
    response = requests.post('http://localhost:9000/register', json=data)
    return response.json()
 
# @app.route('/file/secureLoad', methods=['POST'])
# def secureLoad():
#response = requests.post('http://localhost:9000/register', json=data)
#response = requests.get('https://api.stackexchange.com/2.3/')
#response.json()
#     return { 'result': body.decode('utf-8').replace('\u0000', '') }

if __name__ == '__main__':
    app.run(debug=True)