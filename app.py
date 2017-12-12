from flask import Flask, render_template, json, request,redirect,session
from werkzeug import generate_password_hash, check_password_hash
from flask import session
from flask_mongoengine import MongoEngine
from mongoengine import connect



app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {'DB': 'todoapp'}

app.config['TESTING'] = True
app.config['SECRET_KEY'] = 'flask+mongoengine=<3'
app.debug = True
app.config['DEBUG_TB_PANELS'] = (
    'flask_debugtoolbar.panels.versions.VersionDebugPanel',
    'flask_debugtoolbar.panels.timer.TimerDebugPanel',
    'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
    'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
    'flask_debugtoolbar.panels.template.TemplateDebugPanel',
    'flask_debugtoolbar.panels.logger.LoggingPanel',
    'flask_mongoengine.panels.MongoDebugPanel'
)

db = MongoEngine()
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/register')
def resgister():
    return render_template('register.html')

@app.route('/about')
def about():
  return render_template('about.html')


@app.route('/saveUser',methods=['POST','GET'])
def saveUser():
    try:
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        if _email and _password:
            # Save to database
            connect('todoapp')
            user = User(email=_email)
            user.password=_password
            user.save()
            return json.dumps({'message':'User created successfully !'})

        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return render_template('error.html',error = str(e))
    #finally:
    #   db_client.close()


@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        if _email and _password:
            connect('todoapp')
            user = User.objects(email=_email)
            if user:
                session['user']=user._id
                redirect('/todoHome')
            else:
                return render_template('error.html',error = 'Bad data or user dont exist.')
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})


    except Exception as e:
        return render_template('error.html',error = str(e))


@app.route('/todoHome')
def todoHome():
    if session.get('user'):
        return render_template('todoHome.html')
    else:
        return render_template('error.html',error = 'No no no !. Unauthorized Access')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

class User(db.Document):
    email = db.StringField(required=True)
    password = db.StringField(max_length=50)

class TodoItem(db.Document):
    item = db.StringField(required=True)
    status = db.BooleanField(default=False)
    user = db.ReferenceField(User)



if __name__ == "__main__":
    app.run()
