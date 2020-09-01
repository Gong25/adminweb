from flask import Flask, render_template, request, redirect,url_for,session,abort
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
import base64
from io import BytesIO
from matplotlib.figure import Figure
import seaborn as sns
from dao import member_dao
import sqlite3
app = Flask(__name__)
app.secret_key = b'34_3erg#edsQ\zde]'



@app.route("/")
def index():
    if ('username' in session and session['role'] == 'admin'):
        return render_template('admin_index.html')
    return render_template("index.html")


@app.route("/graph")
def graph():
    if not ('username' in session):
        return redirect('/login')
    poverty_lever = pd.read_csv('static/PercentagePeopleBelowPovertyLevel.csv', encoding='windows-1252')
    poverty_lever.poverty_rate.replace(['-'],0.0,inplace=True)
    poverty_lever.poverty_rate = poverty_lever.poverty_rate.astype(float)
    area_list = list(poverty_lever['Geographic Area'].unique())
    area_poverty_rate_ratio = []
    for i in area_list:
        x = poverty_lever[poverty_lever['Geographic Area'] == i]
        area_poverty_rate = sum(x.poverty_rate)/len(x)
        area_poverty_rate_ratio.append(area_poverty_rate)

    data = pd.DataFrame({'area_list' : area_list, 'area_poverty_rate_ratio':area_poverty_rate_ratio})
    new_index = (data['area_poverty_rate_ratio'].sort_values(ascending=False)).index.values
    sort_data = data.reindex(new_index)

    plt.figure(figsize=(10,3))
    sns.barplot(x=sort_data['area_list'],y=sort_data['area_poverty_rate_ratio'])
    # plt.savefig(fname="D:\coronaweb\static" , format="png")
    buf = BytesIO()
    plt.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    result = {'data' : data}
    return render_template('graph.html', result=result)

@app.route("/login")
def log_in():
    return render_template("login.html")

@app.route("/logout")
def log_out():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('index'))



@app.route("/proclogin", methods = ['POST'])
def proc_login():
    username = request.form['id']
    password = request.form['passwd']
    member = member_dao.select_member_by_db(username,password)
    
    # print(member['password'])
    if member is None:
        error = "아이디 또는 비밀번호가 틀렸습니다"
        return render_template('login.html', error=error)

    elif member is not None:
        session['username'] = member['name']
        session['role'] = member['role']
        return redirect('/admin_index')

@app.route('/admin_index')
def admin_index():
    return render_template('/admin_index.html')

@app.route('/member_view')
def member_view():
    if not ('username' in session):
        return redirect('/login')
    conn = sqlite3.connect('projectC.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT * FROM member')
    rows = cur.fetchall()
    return render_template('member_view.html', rows = rows)

@app.route('/member_add')
def member_add():
    if not ('username' in session):
        return redirect('/login')
    return render_template('member_add.html')

@app.route('/proc_member_add', methods = ['POST'])
def proc_member_add():
    name = request.form['name']
    age = request.form['age']
    phone = request.form['phone']
    add_member = member_dao.add_member(name,age,phone)
    return redirect('/member_view')

@app.route('/proc_member_del', methods = ['POST'])
def proc_member_del():
    no = request.form.getlist('check[]')
    # print('no:',no)
    for i in no:
        del_member = member_dao.del_member(i)
    return redirect('/member_view')



#비디오 관련 페이지

@app.route('/video_view')
def video_view():
    if not ('username' in session):
        return redirect('/login')
    conn = sqlite3.connect('projectC.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT * FROM video')
    rows = cur.fetchall()
    return render_template('member_view.html', rows = rows)



