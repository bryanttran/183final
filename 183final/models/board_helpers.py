from datetime import datetime
from datetime import date


def edit_board_form(id):
    """Returns an SQLFORM used to modify the given entry id"""
    q = db.boards(id)
    form = SQLFORM(db.boards, q)
    form.vars.brd_time = datetime.utcnow()
    if form.process().accepted:
        session.flash = "Board modified!"
        db(db.boards.id == id).update(brd_time=datetime.utcnow())
        redirect(request.env.http_referer)
    return form


def edit_message_form(message):
    """Returns an SQLFORM used to modify the given entry id"""
    q = db.messages(message.id)
    form = SQLFORM(db.messages, q)
    form.vars.msg_time = datetime.utcnow()
    if form.process().accepted:
        session.flash = "Message modified!"
        # Update board time
        db(db.boards.id == message.msg_brd).update(brd_time=datetime.utcnow())
        redirect(request.env.http_referer)
    return form


def get_user_from_id(id):
    """Returns a string of the user name given a web2py id"""
    data = db.auth_user(id)
    name = '{} {}'.format(data.first_name, data.last_name)
    return name


def get_board_message_today_count(board):
    """Returns a count of the messages last edited today in the given board"""
    today = date.today()
    data = db((db.messages.msg_brd == board['id']) &
              (db.messages.msg_time.year() == today.year) &
              (db.messages.msg_time.month() == today.month) &
              (db.messages.msg_time.day() == today.day)).select()
    return len(data)


def get_num_messages(board):
    return len(db(db.messages.msg_brd == board['id']).select())

