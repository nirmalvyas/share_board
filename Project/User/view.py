from flask import Blueprint,g,request
from models import User,Notes,UserNotes
from appholder import *
import json
import hashlib
from util import generate_password_hash,validate_access_for_notes
import uuid
from flask import Response
user_blueprint= Blueprint('user', __name__)



@user_blueprint.route('/users',methods=['POST','GET','PUT','DELETE','OPTIONS'])
def user_register():
    if request.method == 'POST': 
        try:
            user_firstname = request.values.get('user_firstname')
            user_lastname = request.values.get('user_lastname')
            user_email = request.values.get('user_email')
            password = request.values.get('password')
            if not user_firstname:
               return json.dumps({'error':'user_firstname_IS_MANDOTRY','status':0})
            elif not user_lastname:
                return json.dumps({'error':'user_lastname_IS_MANDOTRY','status':0})
            elif not password:
                return json.dumps({'error':'passord_IS_MANDOTRY','status':0})
            else:
                #check length for password
                pass_length = len(password)
                if pass_length < 3 or pass_length > 10:
                    return json.dumps({'error':'PASSWORD_SHOULD_BE_BETWEEN_LENGTH_3_TO_10','status':0})

            l = User.query.filter_by(user_email=user_email).one_or_none()
            if l is None:
                #hash the password and then store
                encrypted_pass = generate_password_hash(password = password)
                if isinstance(encrypted_pass,bool):
                    return json.dumps({'error':'SOMETHING_WENT_WRONG_IN_STORING_DATA_WHILE REGISTER','status':0})
                l = User(user_firstname=user_firstname, user_lastname=user_lastname, user_email=user_email,password=encrypted_pass)
            else:
                return json.dumps({'errors': 'USERNAME_ALREADY_EXISTS', 'status': 0})
            db.session.add(l)
            db.session.commit()
            js={'status':1,'message':'User Created'}
            return json.dumps(js)

        except Exception as e:
            print "==Something went wrong==",str(e)
            return json.dumps({'error':'SOMETHING_WENT_WRONG_IN_LOGGING_USER','status':0})
    
    elif request.method == 'GET':
        # get all the details for the user
        result_set_data =[]
        q = db.session.query(User.user_firstname,User.user_lastname,User.user_email,User.id) 
        result_set = q.all()
        if result_set:
            result_set_data = [u._asdict() for u in result_set]
        return json.dumps({'status':1,'data':result_set_data})

    elif request.method == 'PUT':
        # EDIT THE USER DETAILS
        user_firstname = request.values.get('user_firstname')
        user_lastname = request.values.get('user_lastname')
        user_email = request.values.get('user_email')
        password = request.values.get('password')
        user_id = request.values.get('user_id')
        if not user_firstname:
               return json.dumps({'error':'user_firstname_IS_MANDOTRY','status':0})
        elif not user_lastname:
            return json.dumps({'error':'user_lastname_IS_MANDOTRY','status':0})
        elif not password:
            return json.dumps({'error':'passord_IS_MANDOTRY','status':0})
        elif not user_id:
            return json.dumps({'error':'user_id_IS_MANDOTRY_FOR_UPDATING RECORDS','status':0})
        else:
            #check length for password
            pass_length = len(password)
            if pass_length < 3 or pass_length > 10:
                return json.dumps({'error':'PASSWORD_SHOULD_BE_BETWEEN_LENGTH_3_TO_10','status':0})
            
             #hash the password and then store
            encrypted_pass = generate_password_hash(password = password)
            if isinstance(encrypted_pass,bool):
                return json.dumps({'error':'SOMETHING_WENT_WRONG_IN_STORING_DATA_WHILE REGISTER','status':0})
        
            q = db.session.query(User).filter(User.id == user_id).update({
                'user_firstname':user_firstname,
                'user_lastname':user_lastname,
                'user_email':user_email,
                'password':encrypted_pass,
            })
            db.session.commit()
            return json.dumps({'status':1,'message':'User Record Updated!!'})
    elif request.values.get == 'DELETE':
        # doing soft delete disable the flag
        user_id = request.values.get('user_id')
        if not user_id:
            return json.dumps({'error':'user_id_IS_MANDOTRY_FOR_DELETING_RECORDS','status':0})
        q = db.session.query(User).filter(User.id == user_id).update({
                'status':'D'
                          })
        db.session.commit()
        return json.dumps({'status':1,'message':'User Record Deleted!!'})

    else:
        return json.dumps({'error':'UNAUTHORISED_METHOD_FOR_ACCESS','status':0})


@user_blueprint.route('/notes',methods=['POST','GET','PUT','DELETE','OPTIONS'])
def user_login():
    if request.method == 'POST': 
        try:
            description = request.values.get('description')
            creater_user_id = request.values.get('user_id')

            if not description:
                return json.dumps({'error':'discription_IS_MANDOTRY','status':0})
            if not creater_user_id:
                return json.dumps({'error':'PLS_GIVE_CURRENT_USER_ID','status':0})
            q = Notes(description=description,creater_user_id=creater_user_id)
            db.session.add(q)
            db.session.commit()
            js={'status':1,'message':'notes created successfully!!'}
            return json.dumps(js)
        except Exception as e:
            print "==SOMETHING WENT WRONG!!",str(e)
            return json.dumps({'error':'SOMETHING_WENT_WRONG_IN_POSTING_NOTES','status':0})
    elif request.method == 'GET':
        # get all the notes
        result_set_data=[]
        q = db.session.query(Notes.description,User.user_firstname,User.id.label('Creator_user_id'))
        q = q.join(User,Notes.creater_user_id == User.id)
        q = q.filter(User.status == 'A').all()
        if q:
            result_set_data = [u._asdict() for u in q]
        return json.dumps({'status':1,'data':result_set_data})

    elif request.method == 'PUT':
        #get user id and notes id of the person editing the notes
        user_id = request.values.get('user_id')
        notes_id = request.values.get('notes_id')
        print "==notes_id",notes_id
        if not user_id:
            return json.dumps({'error':'user_id_IS_MANDOTRY_FOR_UPDATING RECORDS','status':0})
        elif not notes_id:
            return json.dumps({'error':'notes_id_IS_MANDOTRY_FOR_UPDATING RECORDS','status':0})
        # check whether the user has right to change the note
        if validate_access_for_notes(user_id=user_id,notes_id=notes_id,action='UPDATE'):
            description = request.values.get('description')
            if not description:
                return json.dumps({'error':'discription_IS_MANDOTRY','status':0})
            q = db.session.query(Notes).filter(Notes.id == notes_id).update({
                'description':description
            })
            db.session.commit()
            return json.dumps({'status':1,'message':'notes updated successfully!!'})

        else:
            return json.dumps({'status':0,'error':'ACCESS_DENIED'})
    
    else:
        return json.dumps({'error':'UNAUTHORISED_METHOD_FOR_ACCESS','status':0})



@user_blueprint.route('/share/notes',methods=['POST','OPTIONS'])
def user_logout():
    if request.method == 'POST': 
        try:
            user_id = request.values.get('user_id')
            notes_id = request.values.get('notes_id')
            write_access = request.values.get('write_access',False)
            delete_access = request.values.get('delete_access',False)
            # check the seesion and if there is active session deactivate them
            if not user_id:
                return json.dumps({'error':'user_id_IS_MANDOTRY','status':0})
            if not notes_id:
                return json.dumps({'error':'notes_id_IS_MANDOTRY','status':0})

            q = UserNotes(user_id = user_id,notes_id=notes_id,write_access=write_access,delete_access=delete_access,read_access=True)
            db.session.add(q)
            db.session.commit()


            return json.dumps({'status':1,'message':'Notes Shared Successully!'})

            

        except Exception as e:
            print "==Something went wrong==",str(e)
            return json.dumps({'error':'SOMETHING_WENT_WRONG_IN_LOGGING_OUT_USER','status':0})

    else:
        return json.dumps({'error':'UNAUTHORISED_METHOD_FOR_ACCESS','status':0})




    