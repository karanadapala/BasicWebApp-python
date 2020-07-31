from flask import Flask, render_template, request, redirect, url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
import sys
import pymysql
from flask import abort
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:password@database-1.c0leffiuwwfn.ca-central-1.rds.amazonaws.com:3306/ansibleproj'


db = SQLAlchemy(app)
migrate = Migrate(app, db)

class UserData(db.Model):
    __tablename__ = 'userdata'
    name = db.Column(db.String(30), primary_key=True)
    color = db.Column(db.String(10), nullable=False)
    animal = db.Column(db.String(5), nullable=False)

db.create_all()

@app.route('/data/submit',methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        print(request.get_json())
        name = request.get_json()['name']
        color = request.get_json()['color']
        animal = request.get_json()['animal']
        names = db.session.query(UserData.name).all()
        for x in names:
            if name.lower() == x[0].lower():
                abort(500)
        #print(names)
        todo = UserData(name=name, color=color,animal=animal)
        db.session.add(todo)
        db.session.commit()
        body['name'] = todo.name
        
    except:    
        db.session.rollback()
        print(sys.exc_info())
        error = True
        
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify(body)    

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True) 