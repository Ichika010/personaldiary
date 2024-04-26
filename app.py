import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask,redirect,url_for,render_template,request,jsonify
from pymongo import MongoClient
from datetime import datetime

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("mongodb://test:sparta@ac-5dlezg7-shard-00-00.plww7op.mongodb.net:27017,ac-5dlezg7-shard-00-01.plww7op.mongodb.net:27017,ac-5dlezg7-shard-00-02.plww7op.mongodb.net:27017/?ssl=true&replicaSet=atlas-wvrwau-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0")
DB_NAME =  os.environ.get("personaldiary")

client = MongoClient('mongodb://test:sparta@ac-5dlezg7-shard-00-00.plww7op.mongodb.net:27017,ac-5dlezg7-shard-00-01.plww7op.mongodb.net:27017,ac-5dlezg7-shard-00-02.plww7op.mongodb.net:27017/?ssl=true&replicaSet=atlas-wvrwau-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0')
db=client.personaldiary

app=Flask(__name__)
@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        # Handle POST Request here
        return render_template('index.html')
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({},{'_id':False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    file = request.files["file_give"]
    extension = file.filename.split('.')[-1]
    filename = f'static/post-{mytime}.{extension}'
    file.save(filename)

    profile = request.files['profile_give']
    extension = profile.filename.split('.')[-1]
    profilename = f'static/profile-{mytime}.{extension}'
    profile.save(profilename)

    doc = {
        'file': filename,
        'profile': profilename,
        'title':title_receive,
        'content':content_receive
    }
    db.diary.insert_one(doc)

    return jsonify({'msg':'Upload complete!'})


if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run('0.0.0.0',port=5000,debug=True)