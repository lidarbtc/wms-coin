from itertools import count
from this import s
from flask import *
import pymysql
import threading, datetime

#시작
app = Flask(__name__)
app.config["SECRET_KEY"] = b'dsf$dsf93334K4WsuG6v3dsfsdfe3fdgfdgdf'
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(minutes=15)

#html 경로 지정
HTML_PATH_LOGIN = './sign/login.html'
HTML_PATH_REGISTER = './sign/register.html'
HTML_PATH_DASHBOARD = './dashboard.html'
HTML_PATH_403 = './error/403.html'
HTML_PATH_404 = './error/404.html'
HTML_PATH_CHART = './chart.html'
#DB 연결
def db_connector(sql_command):
    MYSQL_DB = {
        'user'     : 'dbuser',
        'password' : 'abcd1234',
        'host'     : 'localhost',
        'port'     : '3306',
        'database' : 'wmscoin'
    }
    db = pymysql.connect(
        host=MYSQL_DB['host'],
        port=int(MYSQL_DB['port']),
        user=MYSQL_DB['user'],
        passwd=MYSQL_DB['password'],
        db=MYSQL_DB['database'],
        charset='utf8'
    )
    cursor = db.cursor()
    cursor.execute(sql_command)
    result = cursor.fetchall()
    db.commit()
    db.close()
    return str(result).replace("(", "").replace(")", "").replace("'", "").replace(',', '').rstrip()

#로그인 확인
def checklogin():
    if 'user' in session:
        return True
    return False

#로그인
@app.route('/', methods=['GET', 'POST']) 
def login():
    if request.method == 'GET':
        if checklogin():
            return render_template(HTML_PATH_DASHBOARD, username=session['user'], countcoin=session['countcoin'])
        return render_template(HTML_PATH_LOGIN)
    elif request.method =='POST':
        userid = request.form.get('username')
        userpw = request.form.get('password')
        data = db_connector(f'''SELECT userid, countcoin FROM usertbl WHERE userid="{userid}" AND userpw="{userpw}";''')
        print(data)
        if data == "":
            return render_template(HTML_PATH_LOGIN, ErrorTitle="ERROR! ", ErrorMessage="Username/Password does not exist")
        else:
            session['user'] = userid
            session['countcoin'] = data.split(' ')[1]
            return render_template(HTML_PATH_DASHBOARD, username=session['user'], countcoin=session['countcoin'])

#회원가입
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method =='GET':
        if checklogin():
            return render_template(HTML_PATH_REGISTER, username=session['user'], countcoin=session['countcoin'])
        return render_template(HTML_PATH_REGISTER)
    elif request.method =='POST':
        userid = request.form.get('username')
        userpw = request.form.get('password')
        reuserpw = request.form.get('repassword')
        if userpw != reuserpw:
            return render_template(HTML_PATH_REGISTER, ErrorTitle="ERROR! ", ErrorMessage="Password is different")
        checkusername = db_connector(f'''SELECT userid FROM usertbl WHERE userid="{userid}";''')
        if checkusername == "":
            db_connector(f"INSERT INTO usertbl(userid, userpw, countcoin) VALUES('{userid}', '{userpw}', '0');")
            return render_template(HTML_PATH_LOGIN, ErrorTitle="NOTICE! ", ErrorMessage="Register Success")
        else:
            return render_template(HTML_PATH_REGISTER, ErrorTitle="ERROR! ", ErrorMessage="Username already exist")

#로그아웃
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user', None)
    return render_template(HTML_PATH_LOGIN)

if __name__ == '__main__':
    app.run(host="localhost", port="3000",debug=False, threaded=True)
