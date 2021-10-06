from app import app
from flask import render_template, redirect, url_for, session, request, Response
import paramiko
import json
import os.path
import sys
from base64 import b64decode, b64encode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from io import StringIO

# transport 열기
host, port = '220.149.241.75', 3302
transport = paramiko.Transport((host, port))

# 사용사 인증
username, password = "aiiaabc_5", "aiia&abc!tjqj5"
transport.connect(None, username, password)

# 시작
sftp = paramiko.SFTPClient.from_transport(transport)

# 홈페이지 로그인 정보 하드코딩
saved_email = 'asd@asd.com'
saved_password = 'asd'


@app.route('/')
def index() :
    return redirect(url_for('IRB'))

@app.route('/irb')
def IRB() :
    signin = False
    if 'IRBsignin' in session :
        signin = True
    
    return render_template("irb.html", IRBsignin=signin)

@app.route('/irb/process-signin', methods=['POST'])
def IRB_processSignin() :
    values = request.get_json(force=True)
    input_email = values['email']
    input_pwd = values['password']

    if (input_email == saved_email and input_pwd == saved_password) :
        session['IRBsignin'] = True
        return redirect(url_for('IRB'))
    else :
        return '<script>alert("Check your inputs");history.go(-1);</script>'

@app.route('/irb/process-signout', methods=['POST'])
def IRB_processSignout() :
    # session.pop('IRBsignin', None)
    # session.pop('IRBinv', None)
    # session.pop('ProviderInv', None)
    # session.pop('Provider_ResearcherCred', None)
    # session.pop('ConsumerSignin', None)
    # # session.pop('prov_cons_Connected', None)
    # session.pop('ConsumerInv', None)
    # session.pop('Consumer_ResearcherCred', None)
    # session.pop('PullData', None)
    session.clear() # 모든 섹션 삭제
    return 'sign out OK'



@app.route('/researcher')
def researcher() :
    return render_template("researcher.html")

@app.route('/researcher/irb')
def researcher_irb() :
    signin = False
    inv = False
    if 'IRBsignin' in session :
        signin = True
    if 'IRBinv' in session:
        inv = True

    print(f'signin: {signin}, inv: {inv}', file=sys.stdout)

    return render_template('researcher_irb.html', IRBsignin=signin, IRBinv=inv)

@app.route('/researcher/provider')
def researcher_provider() :
    inv = False
    if 'ProviderInv' in session :
        inv = True
    return render_template('researcher_provider.html', ProviderInv=inv)

@app.route('/researcher/consumer')
def researcher_consumer() :
    signin = False
    inv = False
    data = False

    content = '' # 빈 파일 content
    download_file = '' # 빈 파일 제목
    if 'ConsumerSignin' in session :
        signin = True

    if 'ConsumerInv' in session :
        inv = True

        # files 폴더에 저장된 credential.json 파일 가져오기 (key1, 2, iv로 구성)
        current_path = os.getcwd() # 현재 working directory 경로 가져오기
        file_path = os.path.join(current_path, 'app', "files", "credential.json") # 경로 병합해 새 경로 생성
        if os.path.isfile(file_path) :
            with open(file_path, 'r') as f :
                content = json.load(f)
            f.close()
    if 'PullData' in session :
        data = True

        # consumer 페이지에서 pull data 세션 생성 후 파일 복호화
        current_path = os.getcwd() # 현재 working directory 경로 가져오기
        file_path = os.path.join(current_path, 'app', "files", "credential.json") # 경로 병합해 새 경로 생성
        data = '' # 빈 데이터
        if os.path.isfile(file_path) :
            with open(file_path, 'r') as f :
                data = json.load(f)
            f.close()
        key1 = b64decode(data['key1'].encode('utf-8'))
        key2 = b64decode(data['key2'].encode('utf-8'))
        iv = b64decode(data['seed'].encode('utf-8'))
        body1, body2 = twoChannelLoad("sCDC0109267107", "secM0803220193")
        body1 = b64decode(body1.encode('utf-8'))
        body2 = b64decode(body2.encode('utf-8'))
        body = twoChannelDecrytion(key1, key2, iv, body1, body2)
        file = { 'result': body.decode('utf-8').replace('\u0000', '') }
        download_file = body.decode('utf-8').replace('\u0000', '')

    return render_template('researcher_consumer.html', ConsumerSignin=signin, ConsumerInv=inv, PullData=data, credential=content, download_file=download_file)

@app.route('/researcher/accept-irb-inv', methods=['POST'])
def researcher_accept_irb_inv() :
    values = request.get_json(force=True)
    session['IRBinv'] = values
    return values

@app.route('/researcher/accept-provider-inv', methods=['POST'])
def researcher_accept_provider_inv() :
    values = request.get_json(force=True)
    session['ProviderInv'] = values
    return values

@app.route('/researcher/accept-con-inv', methods=['POST'])
def researcher_accept_con_inv() :
    values = request.get_json(force=True)
    session['ConsumerInv'] = values
    return values

@app.route('/researcher/download-file', methods=['POST'])
def researcher_download_file() :
    values = request.get_json(force=True)
    file = values['file'] # extract file value only

    # SFTP
    sftp_path = f'/repo_test/{file}' # SFTP 서버 경로

    file_path = os.path.abspath("/Users/labia/Public")
    file_path = os.path.join(file_path, file) # 경로 병합해 새 경로 생성

    print(file_path, file=sys.stdout)
    sftp.get(sftp_path, file_path) # 파일 다운로드

    return "download OK"

@app.route('/researcher/upload-file', methods=['POST'])
def researcher_upload_file() :
    values = request.get_json(force=True)
    file = values['files'] # extract file value only
    files = file.split(',') # split them by ,
    files.pop() # and remove the last element because it's empty
    print(files, file=sys.stdout)

    for file in files :
        local_path = os.path.abspath(file)
        sftp_path = '/' + file
        sftp.put(local_path, sftp_path)


    # # SFTP
    # sftp_path = '/' + files[0]
    # file_path = files[0]
    # sftp.put(file_path, sftp_path)
    return files[1]


@app.route('/provider')
def provider() :
    inv = False
    cred = False
    connected = False
    if 'ProviderInv' in session :
        inv = True
    if 'Provider_ResearcherCred' in session :
        cred = True
    # if 'prov_cons_Connected' in session :
    #     connected = True
    return render_template('provider.html', ProviderInv=inv, ResearcherCred=cred, prov_cons_Connected=connected)

@app.route('/provider/create-inv', methods=['POST'])
def provider_create_inv() :
    values = request.get_json(force=True)
    return values

@app.route('/provider/receive-cred', methods=['POST'])
def provider_receive_cred() :
    credential = request.get_json(force=True)['credential']
    session['Provider_ResearcherCred'] = credential
    return credential

@app.route('/provider/send-credential', methods=["POST"])
def provider_select_file() :
    file = request.get_json(force=True) # 웹  페이지로부터 값  받아오기
    title = file["file"] # file 제목만 꺼내기

    sftp_path = f'/repo_test/{title}' # SFTP 서버 경로

    current_path = os.getcwd() # 현재 working directory 경로 가져오기
    file_path = os.path.join(current_path, 'app', "files", title) # 경로 병합해 새 경로 생성

    sftp.get(sftp_path, file_path) # 파일 다운로드

    # 암호화

        # 1) 파일 내용 읽어오기
    body = '' # empty data content
    f = open(file_path, "r")
    while True :
        line = f.readline()
        if line == '' : break # 빈 줄이라면 반복문 멈추기
        body += line
    body = body.encode('utf-8')

        # 2) 2개의 키, 데이터 생성
    key1 = b64decode("othk6WkHQ4O6Iz//KZWpaM2fLXLQw80rD8Bt/XLtSuo=".encode('utf-8'))
    iv = b64decode("XYsr8+TbMFcCd9DHiCZGzg==".encode('utf-8'))
    key2 = b64decode("fbYeFx+06LRa47rZZH3Db6xO0rezOIitQ27r07ZEpbw=".encode('utf-8'))
    body1, body2 = twoChannelEncrytion(key1, key2, iv, body)

    twoChannelStore(b64encode(body1).decode('utf-8'), b64encode(body2).decode('utf-8'))
    
        # credential을 files 폴더에 파일로 저장
    credential_path = os.path.join(current_path, 'app', "files", "credential.json") # 경로 병합해 새 경로 생성
    with open(credential_path, 'w', encoding='utf-8') as f :
        content = {
            'key1': b64encode(key1).decode('utf-8'),
            'key2': b64encode(key2).decode('utf-8'),
            'seed': b64encode(iv).decode('utf-8')
        }
        content = json.dumps(content, ensure_ascii=False, indent="\t") # json으로 변환
        f.write(content) # 파일에 쓰기
    f.close() # 파일 닫기
    return content

# 키 암호화 함수
def encrypt(key, iv, bMessage):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    tail = 16 - (len(bMessage) % 16)
    #print(tail)
    plain = bMessage + bytes(tail)
    #print(plain)

    cMessage = encryptor.update(plain) + encryptor.finalize()
    return cMessage

# 키 복호화 함수
def decrypt(key, iv, cMessage):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    return decryptor.update(cMessage) + decryptor.finalize()

# 암호화 함수
def twoChannelEncrytion(key1, key2, iv, body):
    # import os
    # key1 = os.urandom(32)
    # iv = os.urandom(16)
    # key2 = os.urandom(32)  
    split = [bytearray(), bytearray()]
    for i in range(len(body)):
        split[i%2].append(body[i])
    body1 = encrypt(key1, iv, split[0])
    body2 = encrypt(key2, iv, split[1])
    # return key1, key2, iv, body1, body2
    return body1, body2

# 복호화 함수
def twoChannelDecrytion(key1, key2, iv, body1, body2):
    split1 = decrypt(key1, iv, body1)
    split2 = decrypt(key2, iv, body2)
    body = bytearray()
    for i in range(len(split1)):
        body.append(split1[i])
        body.append(split2[i])
    return body

def twoChannelStore(body1, body2):
    current_path = os.getcwd() # 현재 working directory 경로 가져오기

    hash1 = "sCDC0109267107"
    hash1_path = os.path.join(current_path, 'app', "files", hash1) # 경로 병합해 새 경로 생성
    file1 = open(hash1_path, 'w')
    file1.write(body1)
    file1.close()
    hash2 = "secM0803220193"
    hash2_path = os.path.join(current_path, 'app', "files", hash2) # 경로 병합해 새 경로 생성
    file2 = open(hash2_path, 'w')
    file2.write(body2)
    file2.close()
    return hash1, hash2
    
def twoChannelLoad(hash1, hash2):
    current_path = os.getcwd() # 현재 working directory 경로 가져오기

    hash1_path = os.path.join(current_path, 'app', "files", hash1) # 경로 병합해 새 경로 생성
    file1 = open(hash1_path, 'r')
    body1 = file1.read()
    file1.close()

    hash2_path = os.path.join(current_path, 'app', "files", hash2) # 경로 병합해 새 경로 생성
    file2 = open(hash2_path, 'r')
    body2 = file2.read()
    file2.close()
    return body1, body2



@app.route('/consumer')
def consumer() :
    signin = False
    cred = False
    connected = False
    if 'ConsumerSignin' in session :
        signin = True
    if 'Consumer_ResearcherCred' in session :
        cred = True
    # if 'prov_cons_Connected' in session :
    #     connected = True
    return render_template('consumer.html', ConsumerSignin=signin, ResearcherCred=cred, prov_cons_Connected=connected)

@app.route('/consumer/process-signin', methods=['POST'])
def consumer_processSignin() :
    values = request.get_json(force=True)
    input_email = values['email']
    input_pwd = values['password']

    if (input_email == saved_email and input_pwd == saved_password) :
        session['ConsumerSignin'] = True
        return 'Consumer Signin OK'
    else :
        return '<script>alert("Check your inputs");history.go(-1);</script>'

@app.route('/consumer/process-signout', methods=['POST'])
def consumer_processSignout() :
    session.pop('ConsumerSignin', None)
    session.pop('ConsumerInv', None)
    session.pop('Consumer_ResearcherCred', None)
    return 'sign out OK'

# @app.route('/consumer/accept-provider-inv', methods=['POST'])
# def consumer_accpet_provider_inv() :
#     values = request.get_json(force=True)
#     session['prov_cons_Connected'] = values
#     return values

@app.route('/consumer/receive-cred', methods=['POST'])
def consumer_receive_cred() :
    credential = request.get_json(force=True)
    session['Consumer_ResearcherCred'] = credential
    return "credential OK"

@app.route('/consumer/pull-data', methods=['POST'])
def consumer_pull_data() :
    session['PullData'] = True
    return 'Pull Data Availbale'