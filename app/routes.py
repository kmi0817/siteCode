from app import app
from flask import render_template, redirect, url_for, session, request

import sys

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

@app.route('/irb/processSignin', methods=['POST'])
def IRB_processSignin() :
    values = request.get_json(force=True)
    input_email = values['email']
    input_pwd = values['password']

    if (input_email == saved_email and input_pwd == saved_password) :
        session['IRBsignin'] = True
        return redirect(url_for('IRB'))
    else :
        return '<script>alert("Check your inputs");history.go(-1);</script>'

@app.route('/irb/processSignout', methods=['POST'])
def IRB_processSignout() :
    session.pop('IRBsignin', None)
    session.pop('IRBinv', None)
    session.pop('ProviderInv', None)
    session.pop('ConsumerSignin', None)
    session.pop('ConsumerInv', None)
    session.pop('ResearcherCred', None)
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
    data = False
    if 'ConsumerSignin' in session :
        signin = True
    if 'PullData' in session :
        data = True    
    return render_template('researcher_consumer.html', ConsumerSignin=signin, PullData=data)

@app.route('/researcher/accept-irb-inv', methods=['POST'])
def researcher_accept_irb_inv() :
    values = request.get_json(force=True)
    session['IRBinv'] = values['invitation']
    return values

@app.route('/researcher/accept-provider-inv', methods=['POST'])
def researcher_accept_provider_inv() :
    values = request.get_json(force=True)
    session['ProviderInv'] = values['invitation']
    return values

@app.route('/researcher/accept-con-inv', methods=['POST'])
def researcher_accept_con_inv() :
    values = request.get_json(force=True)
    session['ConsumerInv'] = values['invitation']
    return values




@app.route('/provider')
def provider() :
    inv = False
    if 'ProviderInv' in session :
        inv = True
    return render_template('provider.html', ProviderInv=inv)

@app.route('/provider/create-inv', methods=['POST'])
def provider_create_inv() :
    values = request.get_json(force=True)
    return values



@app.route('/consumer')
def consumer() :
    signin = False
    cred = False
    if 'ConsumerSignin' in session :
        signin = True
    if 'ResearcherCred' in session :
        cred = True
    return render_template('consumer.html', ConsumerSignin=signin, ResearcherCred=cred)

@app.route('/consumer/processSignin', methods=['POST'])
def consumer_processSignin() :
    values = request.get_json(force=True)
    input_email = values['email']
    input_pwd = values['password']

    if (input_email == saved_email and input_pwd == saved_password) :
        session['ConsumerSignin'] = True
        return 'Consumer Signin OK'
    else :
        return '<script>alert("Check your inputs");history.go(-1);</script>'
        # 근데 되돌아가진 않음...

@app.route('/consumer/receive-cred', methods=['POST'])
def consumer_receive_cred() :
    credential = request.get_json(force=True)['credential']
    session['ResearcherCred'] = credential
    return credential

@app.route('/consumer/pull-data', methods=['POST'])
def consumer_pull_data() :
    session['PullData'] = True
    return 'Pull Data Availbale'