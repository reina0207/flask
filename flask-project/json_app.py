# flaskのインポート
from flask import Flask

# htmlファイルをレンダリングするためのライブラリ
from flask import render_template, request,redirect,url_for
import json

# アプリオブジェクトの作成
app = Flask(__name__)

# ルーティング
# @app.route('/')
# def hello():
#     name = "Hello World"
#     return name


@app.route('/hive')
def hive():
    return render_template('index.html')

#変数を渡すURL
@app.route('/var')
def var():
    message="お疲れ様"
    return render_template('var.html',message=message)


#If文を利用するURL
@app.route('/greeting_if')
def greeting_if():
    message="おはよう"
    return render_template('greeting_if.html',message=message)


#For文を利用するURL
@app.route('/greeting_for')
def greeting_for():
    message_list=["おはよう","こんにちは","こんばんは"]
    return render_template('greeting_for.html',message_list=message_list)

#FizzBuzz
@app.route('/fizzbuzz')
def fizzbuzz():
    fizzbuzz_message=['FIZZ','BUZZ','FIZZBUZZ']
    return render_template('fizzbuzz.html',fizzbuzz_message=fizzbuzz_message)

#get
# @app.route('/get')
# def get():
#     #GETリクエストを格納
#     #name=request.args.get('name')
#     number=int(request.args.get('number'))
#     number2=list(range(2,number))
#     return render_template('get.html',title='Flask GET request',number=number,number2=number2)

#素数1
# @app.route('/get')
# def get():
#    number=int(request.args.get('number'))
#    for p in range(2, number):
#        if number % p == 0:
#            i='合成数'
#            return render_template('get2.html',title='Flask GET request',i=i)
#    i='素数'
#    return render_template('get2.html',title='Flask GET request',i=i)

#素数２
@app.route('/get')
def get():
    number=int(request.args.get('number'))
    i='素数'
    for p in range(2,number):
        if number % p ==0:
            i='合成数'
    return render_template('get2.html',title='Flask GET request',i=i)

#プロフィールを取得
def get_profile():
    #JSONファイルの読み込み
    file_json="data/profile.json"
    prof=open(file_json,encoding='utf-8')
    json_str=prof.read()
    prof.close()
    #JSON(配列)から辞書型リストに変換
    prof_dict=json.loads(json_str)
    return prof_dict 

#JSONファイルの更新
def update_profile(prof):
    f=open('data/profile.json','w')
    json.dump(prof,f)
    f.close()

#データ一覧画面へリダイレクト
@app.route('/')
def root():
    return redirect(url_for("profile"))

#データ一覧画面
@app.route('/profile')
def profile():
    prof_dict=get_profile()
    return render_template('json_profile.html',title='json',users=prof_dict)

#データ編集画面
@app.route('/edit/<int:id>')
def edit(id):
    prof_dict=get_profile()
    user_dict=""
    for data in prof_dict:
        if data['id']==id:
            user_dict=data
    return render_template('json_edit.html',title='json',user=user_dict)

#データ更新処理
@app.route('/update',methods=['POST'])
def update():
    #POSTで送信されたデータを受け取り、変数に格納
    id_str = request.form['id']
    name = request.form['name']
    age = request.form['age']
    sex = request.form['sex']

    #データを更新してJSONファイルを上書き
    prof_dict_before = get_profile()
    prof_dict_after = []

    for data in prof_dict_before:
        if str(data['id']) == id_str:
            prof_dict_after.append({"id":int(id_str),"name":name,"age":age,"sex":sex})
        else:
            prof_dict_after.append(data)
    update_profile(prof_dict_after)

    #データ更新したら/profile画面に戻る（リダイレクト）
    return redirect(url_for("profile"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True) 

