from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

sapp = app


sapp.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///signup.db"
sapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
sdb= SQLAlchemy(sapp)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

class SignupDB(sdb.Model):
    uname = sdb.Column(sdb.String(100), primary_key=True)
    email = sdb.Column(sdb.String(50), nullable=False)
    passwd = sdb.Column(sdb.String(20), nullable=False)
    conpass = sdb.Column(sdb.String(20), nullable=False)

    def __repr__(self) -> str:
        return f"{self.uname} - {self.email}"

@app.route('/', methods=['GET','POST'])
def login():
    uname_email=""
    passwd=""
    if(request.method=="POST"):
        uname_email = request.form['username']
        passwd = request.form['password']
        exists = sdb.session.query(SignupDB.uname).filter_by(passwd=passwd).first() is not None
        if(exists):
            return redirect(url_for('note_app'))
        else:
            return "Incorrect Credentials"
    
    return render_template("login.html")

@app.route('/signup', methods=['GET','POST'])
def signup():
    return render_template('signup.html')

@app.route('/thankyou', methods=['GET','POST'])
def thankyou():
    if(request.method=="POST"):
        uname = request.form['Username']
        email = request.form['email']
        passwd = request.form['password']
        conpass = request.form['password']
        signup = SignupDB(uname=uname, email=email, passwd=passwd, conpass=conpass)
        sdb.session.add(signup)
        sdb.session.commit()
    return render_template("thankyou.html")

@app.route('/todo', methods=['GET','POST'])
def note_app():
    if request.method=="POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title, desc = desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template("index.html", allTodo=allTodo)

@app.route('/delete', methods=['GET','POST'])
def delete():
    return render_template('delete.html')

@app.route('/deletesno', methods=['GET','POST'])
def deletesno():
    if request.method=="POST":
        dsno = request.form['dsno']
        Todo.query.filter(Todo.sno == dsno).delete()
        db.session.commit()
    
    return redirect(url_for('note_app'))
        
        

if __name__ == "__main__":
    app.run(debug=True)