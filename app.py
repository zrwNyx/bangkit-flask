from flask import Flask,jsonify,request
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)



@app.get("/")
def home():
    return "hello world!"

@app.route('/getalldata', methods = ['GET'])
def ReturnJSON():
    if(request.method == 'GET'):
        with connection:
            with connection.cursor() as cur:
                cur.execute('SELECT * FROM crime;')
                data = cur.fetchall()
                cur.close()
    return data

@app.route('/getid', methods=['POST'])
def getDataByID():
    data = request.get_json()
    no = data["no"]
    with connection:
        with connection.cursor() as cur:
            cur.execute('SELECT * FROM crime WHERE no = (%s);',
                        (str(no),))
            fetched = cur.fetchall()
    return fetched
    
@app.route('/add', methods=['POST'])
def addData():
    data = request.get_json()
    no = data["no"]
    category = data["category"]
    dates = data["dates"]
    hours = data["hours"]
    labels = data["labels"]
    x = data["x"]
    y = data["y"]
    with connection:
        with connection.cursor() as cur:
            cur.execute('INSERT INTO crime (no,category,dates,hours,label,x,y)'
                        'VALUES (%s,%s,%s,%s,%s,%s,%s);',
                        (str(no),str(category),str(dates),str(hours),str(labels),str(x),str(y),))
    return {"no":no,"message":"data has been added"},201

@app.route('/adduser', methods=['POST'])
def addUser():
    data = request.get_json()
    id = data["id"]
    passw = data["passw"]
    with connection:
        with connection.cursor() as cur:
            cur.execute('INSERT INTO userid (username,password)'
                        'VALUES (%s,%s);',
                        (str(id),str(passw),))
    return {"id":id,"message":"user has been created"},201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    id = data["id"]
    passw = data["passw"]
    with connection:
        with connection.cursor() as cur:
            cur.execute('SELECT * FROM userid WHERE username = (%s) AND password = (%s)',
                        (str(id),str(passw),))
            fetched = cur.fetchall()
    try:
        if fetched[0][0] is not None:
            return {"message":"login succesful"}
    except IndexError as e:
        return {"message":"login failed"}
