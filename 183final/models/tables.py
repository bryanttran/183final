#########################################################################
## Define your tables below; for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

from datetime import datetime

#  a Here istable for messages.
db.define_table('boards',
    Field('creator',  db.auth_user, default=auth.user_id),
    Field('brd_time', 'datetime', default=datetime.utcnow()),
    Field('brd_name', 'text', required=True),
    Field('brd_desc', 'text'))

db.boards.id.readable = db.boards.id.writable = False
db.boards.creator.readable = db.boards.creator.writable = False
db.boards.brd_time.readable = db.boards.brd_time.writable = True
db.boards.brd_name.readable = db.boards.brd_name.writable = True
db.boards.brd_desc.readable = db.boards.brd_desc.writable = True
db.boards.brd_time.label = "Time"
db.boards.brd_name.label = "Name"
db.boards.brd_desc.label = "Description"

db.define_table('messages',
    Field('creator', db.auth_user, default=auth.user_id),
    Field('msg_time', 'datetime', default=datetime.utcnow()),
    Field('msg_brd', 'text', required=True),
    Field('msg_title', 'text', required=True),
    Field('msg_id', 'text'),
    Field('image', 'upload'))

#http://stackoverflow.com/questions/6334360/web2py-how-should-i-display-an-uploaded-image-that-is-stored-in-a-database

db.messages.id.readable = db.messages.id.writable = False
db.messages.msg_brd.readable = db.messages.msg_brd.writable = False
db.messages.msg_time.readable = db.messages.msg_time.writable = False
db.messages.creator.readable = db.messages.creator.writable = False
db.messages.msg_id.readable = True
db.messages.msg_time.label = "Time"
db.messages.msg_title.label = "Title"
db.messages.msg_id.label = "Message"

def get_text(v):
    r = db2.textblob(v)
    return '' if r is None else r.mytext

db2.define_table('textblob',
    Field('mytext', 'text'),
    )
