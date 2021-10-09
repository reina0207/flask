from flask import Flask, render_template,request,redirect,url_for
import sqlite3
import datetime
import os

app=Flask(__name__)

#データ取り出し
def get_profile():
    conn = sqlite3.connect('profile.sqlite3')
    c = conn.cursor()
    prof_list=[]
    for i in c.execute('select * from persons;'):
        prof_list.append({'id':i[0],'name':i[1],'age':i[2],'sex':i[3]})
    conn.commit()
    conn.close()
    return prof_list

#レコード更新
def update_profile(prof):
    conn = sqlite3.connect('profile.sqlite3')
    c = conn.cursor()
    c.execute("update persons set name='{0}',age={1},sex='{2}' where id={3};".format(prof['name'],prof['age'],prof['sex'],prof['id']))
    conn.commit()
    conn.close()

#レコード追加　
def add_profile(prof):
    conn = sqlite3.connect('profile.sqlite3')
    c = conn.cursor()
    sql="insert into persons (name,age,sex) values ('{0}','{1}','{2}');".format(prof['name'],prof['age'],prof['sex'])
    # import pdb;pdb.set_trace()
    print(sql)
    c.execute(sql)
    conn.commit()
    conn.close()

#レコード削除
def delete_profile(id):
    conn = sqlite3.connect('profile.sqlite3')
    c = conn.cursor()
    
    c.execute("delete from persons where id={0};".format(id))
    conn.commit()
    conn.close()

#IDから辞書を出す
def id_profile(id,prof_list):
    for i in range(len(prof_list)):
        if prof_list[i]["id"]==id:
            return prof_list[i]
        else:
            pass



@app.route('/')
def top():
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    prof_dict = get_profile()
    dt_now=datetime.datetime.now()
    return render_template('sql_profile.html',title='sql',user=prof_dict,time_stamp=dt_now)

@app.route('/edit/<int:id>')
def edit(id):
    prof_list = get_profile()

    prof_dict = id_profile(id,prof_list)
    dt_now=datetime.datetime.now()
    return render_template('sql_edit.html',title='sql',user=prof_dict,time_stamp=dt_now)

@app.route('/update/<int:id>',methods=['POST'])
def update(id):
    prof_list = get_profile()
    prof_dict = id_profile(id,prof_list)
    #prof_dictの値を変更
    prof_dict['name'] = request.form['name']
    prof_dict['age'] = request.form['age']
    prof_dict['sex'] = request.form['sex']
    update_profile(prof_dict)
    return redirect(url_for("profile"))


@app.route('/new/')
def new():
    return render_template('sql_add.html',title='sql')    


@app.route('/add/',methods=['POST'])
def add():
    #prof_dictに値を追加
    prof_dict={'name':request.form['name'],'age':request.form['age'],'sex':request.form['sex']}
    add_profile(prof_dict)
    return redirect(url_for("profile"))

@app.route('/delete/<int:id>')
def delete(id):
    # import pdb;pdb.set_trace()
    delete_profile(id)
    
    return redirect(url_for("profile"))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)), threaded=True)