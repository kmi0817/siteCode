from app import app
from flask import render_template, redirect, url_for, session, request
import paramiko
import os.path
import sys

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
    session.pop('IRBsignin', None)
    session.pop('IRBinv', None)
    session.pop('ProviderInv', None)
    session.pop('Provider_ResearcherCred', None)
    session.pop('ConsumerSignin', None)
    # session.pop('prov_cons_Connected', None)
    session.pop('ConsumerInv', None)
    session.pop('Consumer_ResearcherCred', None)
    session.pop('PullData', None)
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
    if 'ConsumerSignin' in session :
        signin = True
    if 'ConsumerInv' in session :
        inv = True
    if 'PullData' in session :
        data = True    
    return render_template('researcher_consumer.html', ConsumerSignin=signin, ConsumerInv=inv, PullData=data)

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
    file = values['files'] # extract file value only
    files = file.split(',') # split them by ,

    # # SFTP
    # sftp_path = '/' + files[0]
    # file_path = files[0]
    # sftp.put(file_path, sftp_path)
    return files[0]

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
    credential = request.get_json(force=True)['credential']
    session['Consumer_ResearcherCred'] = credential
    return credential

@app.route('/consumer/pull-data', methods=['POST'])
def consumer_pull_data() :
    session['PullData'] = True
    return 'Pull Data Availbale'