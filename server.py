from flask import Flask, request
from dataRepository import *

app = Flask("server")

@app.route('/newUser', methods=['POST'])
def registerNewUser():
    username = request.form['username']
    password = request.form['password']
    rightsLevel = int(request.form['rightsLevel'])
    if getUser(username) != None:
        return {
            'status': 'error',
            'description': 'user with this name alredy exists'
        }
    User.create(username = username, password = password, rightsLevel = rightsLevel).save()
    
    return {
            'status': 'ok',
            'description': ""
        }

@app.route('/authUser', methods=['POST'])
def userAuth():
    username = request.form['username']
    password = request.form['password']
    user: User = getUser(username)
    if not user or user.password != password:
        return {'status': 'error',
            'description': 'password or username is incorrect'
            }
    return {
        'status': 'ok',
        'description': None,
        'id': user.id,
        'rightsLevel': user.rightsLevel
    }
app.run()