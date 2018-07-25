from appholder import *
# from Movies.views import movies_blueprint


from sqlalchemy import Column, DateTime, Integer, String, text,Float,Boolean





    

class User(db.Model):
    __tablename__ = 'user_details'

    id = Column(Integer, primary_key=True, name='id')
    user_firstname = Column(String(50), name='user_firstname')
    user_lastname = Column(String(50), name='user_lastname')
    user_email = Column(String(20), name='user_email')
    password = Column(String(20), name='password')

    update_dttm = Column(DateTime(True), server_default=text("now()"), name='update_dttm')
    create_dttm = Column(DateTime(True), server_default=text("now()"), name='create_dttm')
    status = Column(String(1), name='status', default='A')

class Notes(db.Model):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, name='id')
    description = Column(String(1000),name='description')
    creater_user_id = Column(Integer,name='creater_user_id')
    update_dttm = Column(DateTime(True), server_default=text("now()"), name='update_dttm')
    create_dttm = Column(DateTime(True), server_default=text("now()"), name='create_dttm')


class UserNotes(db.Model):
    __tablename__ = 'user_notes'

    id = Column(Integer, primary_key=True, name='id')
    user_id = Column(Integer,name='user_id')
    notes_id = Column(Integer,name='notes_id')
    read_access = Column(Boolean,name='read_access')
    write_access = Column(Boolean,name='write_access')
    delete_access = Column(Boolean,name='delete_access')
    update_dttm = Column(DateTime(True), server_default=text("now()"), name='update_dttm')
    create_dttm = Column(DateTime(True), server_default=text("now()"), name='create_dttm')





if __name__ == '__main__':
   manager.run()