import re
from app import app
from flask import render_template, redirect, url_for, session, request

# Researchers Login to IRB
user_id = 'asd'
user_pwd = 'asd'

@app.route('/')
def index() :
    return render_template('index.html')


# irb
@app.route('/irb')
def irb_index() :
    if 'irbLogin' in session :
        return render_template('irb/index.html', login=True)
    else :
        return render_template('irb/index.html', login=False)

@app.route('/irb/processLogin', methods=['POST'])
def irb_processLogin() :
    id = request.form['id']
    pwd = request.form['password']

    if user_id == id and user_pwd == pwd :
        session["irbLogin"] = True
        return redirect(url_for('irb_index'))
    else :
        return '<script>alert("아이디나 비밀번호가 틀립니다.");history.go(-1);</script>'

@app.route('/irb/processLogout')
def irb_processLogout() :
    session.pop('irbLogin', None)
    return redirect(url_for('irb_index'))

@app.route('/irb/copyInvitation', methods=['POST'])
def irb_copyInvitation() :
    return redirect(url_for('researcher_irb'))
    


# provider
@app.route('/provider')
def provider_index() :
    return render_template('providerServer/index.html')

@app.route('/provider/invitation')
def provider_invitation() :
    return render_template('providerServer/creatInv.html')

@app.route('/provider/datalist')
def provider_datalist() :
    return render_template('providerServer/datalist.html')


# researcher
@app.route('/researcher')
def researcher_index() :
    return render_template('researcher/index.html')

@app.route('/researcher/irb')
def researcher_irb() :
    return render_template('researcher/irb.html')

@app.route('/researcher/provider')
def researcher_provider() :
    return render_template('researcher/provider.html')

@app.route('/researcher/consumer')
def researcher_consumer() :
    return render_template('researcher/consumer.html')



# consumer
@app.route('/consumer')
def consumer_index() :
    if 'consumerLogin' in session :
        return render_template('consumerServer/index.html', login=True)
    else :
        return render_template('consumerServer/index.html', login=False)

@app.route('/consumer/processLogin', methods=['POST'])
def consumer_processLogin() :
    id = request.form['id']
    pwd = request.form['password']

    if user_id == id and user_pwd == pwd :
        session["consumerLogin"] = True
        return redirect(url_for('researcher_consumer'))
    else :
        return '<script>alert("아이디나 비밀번호가 틀립니다.");history.go(-1);</script>'

@app.route('/consumer/processLogout')
def consumer_processLogout() :
    session.pop('consumerLogin', None)
    return redirect(url_for('consumer_index'))