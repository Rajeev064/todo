from flask import *
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class login(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(200),nullable = False)
    email_id = db.Column(db.String(200),nullable = False)
    password = db.Column(db.String(200),nullable = False)

    def __repr__(self):
        return '<Email %r>'% self.id

class Todo(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    content = db.Column(db.String(200),nullable = False)
    completed = db.Column(db.Integer,default = 0)
    date_created = db.Column(db.DateTime,default = datetime.utcnow)
    user_id = db.Column(db.Integer,nullable = False)

    def __repr__(self):
        return '<Task %r>' % self.id

#TODO
"""
    add error msg in register,login
"""
@app.route('/',methods=['POST','GET'])
def register():
    if request.method =='POST':
        new_username = request.form['username']
        email = request.form['email']
        new_password = request.form['password']
        new_contact = login(username = new_username,email_id = email,password = new_password)
        r = login.query.filter_by(email_id = email).first()
        if r == None:
            try:
                db.session.add(new_contact)
                db.session.commit()
                flash("Email Added ,now login")
                return render_template('login.html')
            except:
                return 'error in registering '

        elif r.id >=1 :
            flash("Email Available!!")
            return render_template('register.html')
        else :
            return render_template('register.html')
    else:
        return render_template('register.html')


@app.route('/login',methods=['POST','GET'])
def user_login():
    if request.method == 'POST' :
        email = request.form['email']
        password = request.form['password']
        check =  login.query.filter_by(email_id = email).first()
        if check == None:
            flash("Email Not available")
            return render_template('login.html')
        else:
            if check.password == password :
                name = str(check.username)
                session["USERNAME"] = check.id
                return redirect('/tasks')
            else :
                flash('Password incorrect')
                return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/logout',methods=['POST','GET'])
def user_logout():
    if "USERNAME" in session:
        session.pop("USERNAME",None)
        flash("Logged out")
        return render_template('login.html')
    else:
        flash("Log In first")
        return render_template('login.html')

##################################  NO UPDATES NEEDED #########################3

@app.route('/tasks',methods=['POST','GET'])
def index ():
    if request.method =='POST':
        task_content = request.form['content']
        if "USERNAME" in session:
            s = session['USERNAME'] 
            new_task = Todo(content = task_content,user_id = s)
        else:
            return redirect('/login')

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/tasks')
        except:
            return 'Issue in script'
    else :
        if "USERNAME" in session:
            s = session['USERNAME'] 
            tasks = Todo.query.filter_by(user_id = s).all()
            # if tasks ==None:
            #     tasks['id'] = 1
            #     tasks ['content'] = 'Demo event for all'
            #     tasks ['data_created'] = datetime.utcnow
            #     tasks['user_id'] = s
            return render_template('index.html',tasks = tasks)
        else :
            return redirect('/login')
@app.route('/delete/<int:id>')
def delete(id):
    if "USERNAME" in session:
        s = session['USERNAME'] 
        task_delete = Todo.query.get_or_404(id)
    else:
        return redirect('/login')

    try:
        db.session.delete(task_delete)
        db.session.commit()
        return redirect('/tasks')
    except:
        return "Problem deleting task"

@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    if "USERNAME" in session:
        s = session['USERNAME'] 
        task = Todo.query.get_or_404(id)
        if request.method =='POST':
            task.content = request.form['content']

            try:
                db.session.commit()
                return redirect('/tasks')
            except:
                return "Error while updating"

        else:

            return render_template('update.html',task = task)
    else:
        return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)

app.secret_key = "user_new_program"

