from flask import Flask,request,jsonify
import os,re,datetime
import db
from models import User


app = Flask(__name__)



if not os.path.isfile('user.db'):
    db.connect()

@app.route("/")
def home():
    return "Hello, Rest CRUD Api tester!"

def isValid(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
      return True
    else:
      return False
    
@app.route("/request", methods=['POST'])
def postRequest():
    req_data = request.get_json()
    email = req_data['username']
    if not isValid(email):
        return jsonify({
            'status': '422',
            'res': 'failure',
            'error': 'Invalid username. Please enter a valid username should look like email'
        })
    pwd = req_data['password']
    active = req_data['active']
    bks = [b.serialize() for b in db.viewall()]
    for b in bks:
        if b['username'] == email:
            return jsonify({
                # 'error': '',
                'res': f'Error ⛔❌! user with Username {email} is already in system!',
                'status': '404'
            })

    bk = User(db.getNewId(),email,pwd, bool(active))
    print('new user: ', bk.serialize())
    db.insert(bk)
    new_bks = [b.serialize() for b in db.view()]
    print('user in system: ', new_bks)
    
    return jsonify({
                # 'error': '',
                'res': bk.serialize(),
                'status': '200',
                'msg': 'Success creating a user!👍😀'
            })    
    
@app.route('/request', methods=['GET'])
def getRequest():
    content_type = request.headers.get('Content-Type')
    users = [b.serialize() for b in db.viewall()]
    if (content_type == 'application/json'):
        json = request.json
        for b in users:
            if b['id'] == int(json['id']):
                return jsonify({
                    # 'error': '',
                    'res': b,
                    'status': '200',
                    'msg': 'Success getting all users!👍😀'
                })
        return jsonify({
            'error': f"Error ⛔❌! user with id '{json['id']}' not found!",
            'res': '',
            'status': '404'
        })
    else:
        return jsonify({
                    # 'error': '',
                    'res': users,
                    'status': '200',
                    'msg': 'Success getting users!👍😀',
                    'no_of_users': len(users)
                })

@app.route('/request/<string:uname>', methods=['GET'])
def getRequestId(uname):
    users = [b.serialize() for b in db.viewall()]
    for b in users:
        if b['username'] == uname:
            return jsonify({
                    # 'error': '',
                    'res': b,
                    'status': '200',
                    'msg': 'Success getting user by username!👍😀'
                })
        else:
            return jsonify({
            'error': f"Error ⛔❌! Book with id '{uname}' was not found!",
            'res': '',
            'status': '404'
        })

@app.route('/request/<string:uname>', methods=['DELETE'])
def deleteRequest(uname):
    req_args = request.view_args
    print('req_args: ', req_args)
    users = [b.serialize() for b in db.viewall()]
    if req_args:
        for b in users:
            if b["username"] == uname:
                db.delete(b[""])
                updated_bks = [b.serialize() for b in db.viewall()]
                print('updated_bks: ', updated_bks)
                return jsonify({
                    'res': updated_bks,
                    'status': '200',
                    'msg': 'Success users by ID!👍😀',
                    'no_of_books': len(updated_bks)
                })
    else:
        return jsonify({
            'error': f"Error ⛔❌! username sent!",
            'res': '',
            'status': '404'
        })

@app.route("/request", methods=['PUT'])
def putRequest():
    req_data = request.get_json()
    email = req_data['username']
    the_id = req_data['id']
    pwd = req_data['password']
    active = req_data['active']
    bks = [b.serialize() for b in db.viewall()]
    for b in bks:
        if b['id'] == the_id:
            bk = User(
                the_id, 
                email, 
                pwd, 
                active
            )
            print('new user: ', bk.serialize())
            db.update(bk)
            new_bks = [b.serialize() for b in db.viewall()]
            print('User in system: ', new_bks)
            return jsonify({
                # 'error': '',
                'res': bk.serialize(),
                'status': '200',
                'msg': f'Success updating the username {email}!👍😀'
            })        
    return jsonify({
                # 'error': '',
                'res': f'Error ⛔❌! Failed to update user with username: {email}!',
                'status': '404'
            })
 