from flask import Flask,request, render_template,redirect,url_for,session

#from flaskext.mysql import MySQL
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'aptechdb'

mysql = MySQL(app)

app.secret_key='mcgamma-04-adebayo'
@app.route('/')
def home():
    if 'loggedin' in session:
        return render_template('mm.html', userid = session['userid'])
    return redirect(url_for('login'))
@app.route('/mm')
def mm():
    return render_template('mm.html',userid = session['userid'])
    #return redirect(url_for('home.html'))

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=='POST':
        details = request.form.get
        sname = details('surname')
        lname = details('lastname')
        phone = details('phone')
        genderone = details('gender')
        eemail = details('myemail')
        passw = details('password')
        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO flasktable(firstname,lastname,
        phoneno,gender,email,password)
         VALUES(%s,%s,%s,%s,%s,%s)''',
         (sname,lname,phone,genderone,eemail,passw))
        mysql.connection.commit()
        cur.close()
        #return f"Done!"
        return render_template('thanks.html',s = sname,l =lname,p = phone,g = genderone,ema=eemail,pp = passw)

    return render_template('signup.html')

@app.route('/login',methods=['POST','GET'])
def login():
    msg = ''
    if request.method == 'POST' and 'myemail' in request.form and 'mypassword' in request.form:
       
        email = request.form.get('myemail')
        passm = request.form.get('mypassword')
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM flasktable WHERE email=%s AND password=%s',(email,passm))
        record = cur.fetchone()
        if record:
            #print('correct')
            
            #return f"Done!"
            session['loggedin']=True
            session['userid']=record[0]
            return redirect(url_for('mm'))
            #return render_template('home.html',userid=session['userid'])
        else:
            msg = "Incorrect email or Password. Try again"
           #return render_template('login.html',msg=msg)
    return render_template('login.html',msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('userid',None)
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)