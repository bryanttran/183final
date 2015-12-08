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

db.define_table('boards',
    Field('board_name', 'string'),
    Field('board_description', 'string'),
    Field('active_draft_description', 'string'),
    Field('active_draft_name', 'string'),
    Field('board_author', db.auth_user, default=auth.user_id),
    Field('board_id'),
    Field('is_draft', 'boolean', default=False)
    )

db.define_table('posts',
    Field('post_title', 'string'),
    Field('post_author', db.auth_user, default=auth.user_id),
    Field('draft_title', 'string'),
    Field('post_description', 'text'),
    Field('draft_description', 'string'),
    Field('board_id', "reference boards"),
    Field('post_id')
    )
