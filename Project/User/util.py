import hashlib
import random
from flask import request as req
import time
import pytz
from pytz import timezone
from datetime import datetime, timedelta,date
from flask import Response
from models import User,UserNotes,Notes
from appholder import *
def generate_password_hash(password=False):
    """
    this function will generate the password hash that we can store in the database,and also
    then we use the same for authentication.
    @params:password:this is mandotry param its basically the raw password
    """
    if not password:
        return False
    unique = 'onionkandalogin'
    key = hashlib.sha256(password + unique).hexdigest()
    return key

def validate_access_for_notes(user_id=False,notes_id=False,action='UPDATE'):
    """
    this will validate the notes
    """
    if not user_id or not notes_id:
        return False
    # checck the access right.
    if action == 'UPDATE':
        q = db.session.query(UserNotes).filter(UserNotes.user_id == user_id)
        q = q.filter(UserNotes.notes_id == notes_id)
        q = q.filter(UserNotes.write_access == True)
        result_set = q.scalar()
        if result_set:
            return True

        else:
            if is_creater_user(user_id=user_id,notes_id=notes_id):
                return True
            return False
    elif action == 'DELETE':
        q = db.session.query(UserNotes).filter(UserNotes.user_id == user_id)
        q = q.filter(UserNotes.notes_id == notes_id)
        q = q.filter(UserNotes.delete_access == True)
        result_set = q.scalar()
        if result_set:
            return True
        else:
            if is_creater_user(user_id=user_id,notes_id=notes_id):
                return True
            return False

def is_creater_user(user_id=False,notes_id=False):
    """
    Check whether the user is the creater of the specific note..
    """
    if not user_id or not notes_id:
        return False
    q = db.session.query(Notes).filter(Notes.id == notes_id)
    q =q.filter(Notes.creater_user_id == user_id)
    result_set = q.scalar()
    if result_set:
        return True
    return False



    
