# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

from datetime import datetime
import json

def index():
    """
    Displays all the boards and allows the user to login/register to edit/create messages/boards.
    """
    logger.info("Session: %r" % session)

    q = (db.boards.id > 0)
    # Dict for generating board list
    boards = db(q).select(orderby=~db.boards.brd_time)

    user_id = auth.user_id

    return dict(boards=boards, user_id=user_id)


@auth.requires_login()
def add_board():
    db.boards.update_or_insert((db.boards.id == request.vars.id),
            creator = auth.user_id,
            brd_name = request.vars.brd_name,
            brd_desc = request.vars.brd_desc,
            brd_time = datetime.utcnow())
    return "ok"


def load_boards():
    """Loads all boards"""
    q = (db.boards.id > 0)
    # Dict for generating board list
    rows = db(q).select(orderby=~db.boards.brd_time)
    d = []
    for r in rows:
        d.append({
            'id': r.id,
            'creator': r.creator,
            'creator_name': get_user_from_id(r.creator),
            'brd_time': r.brd_time,
            'brd_name': r.brd_name,
            'brd_desc': r.brd_desc,
            'message_num': get_num_messages(r),
            'message_num_today': get_board_message_today_count(r)
        })
    brd_len = len(d)
    return response.json(dict(brd_dict=d, brd_len=brd_len))


@auth.requires_signature()
def delete_board():
    logger.info("Deleting board %r", (db.boards(request.args(0)).id))
    # Remove the board
    db(db.boards.id == request.args(0)).delete()
    # Remove all messages in regards to the board
    db(db.messages.msg_brd == request.args(0)).delete()
    redirect(request.env.http_referer)
    return


@auth.requires_signature()
def delete_boards():
    board_ids = request.vars['boards[]']
    if board_ids:
        if isinstance(board_ids, list):
            for id in board_ids:
                logger.info("Deleting message %r", (id))
                # Remove the board
                db(db.boards.id == id).delete()
                # Remove all messages in regards to the board
                db(db.messages.msg_brd == id).delete()
            return "ok"
        else:
            # Remove the board
            db(db.boards.id == board_ids).delete()
            # Remove all messages in regards to the board
            db(db.messages.msg_brd == board_ids).delete()
            return "ok"
    else:
        session.flash = "Error deleting post!"
        return ""

@auth.requires_signature()
def delete_messages():
    message_ids = request.vars['messages[]']
    if message_ids:
        if isinstance(message_ids, list):
            for id in message_ids:
                logger.info("Deleting message %r", (id))
                # Remove the message
                db(db.messages.id == id).delete()
            return "ok"
        else:
            # Remove the board
            db(db.messages.id == message_ids).delete()
            return "ok"
    else:
        session.flash = "Error deleting message!"
        return ""

def create_post():
    back_button = A('Go back', _class="btn btn-default", _href=URL('default', 'boards'))
    form = SQLFORM(db.posts, fields=['title', 'description', 'image'])
    if form.process().accepted:
        redirect(URL('boards'))
    return dict(form=form, back_button=back_button)

@auth.requires_signature()
def delete_message():
    logger.info("Deleting message %r", (db.messages(request.args(0)).id))
    # Remove the message
    db(db.messages.id == request.args(0)).delete()
    redirect(request.env.http_referer)
    return


@auth.requires_login()
def add_message():
    db.messages.update_or_insert((db.messages.id == request.vars.id),
            creator = auth.user_id,
            msg_title = request.vars.msg_title,
            msg_id = request.vars.msg_desc,
            msg_time = datetime.utcnow(),
            msg_brd = request.vars.msg_brd)
    return "ok"


def boards():
    """This page enables you to view/edit the contents of a board."""
    # grab messages pertaining to the board
    messages = db(db.messages.msg_brd == request.args(0)).select()
    title = db.boards(request.args(0)).brd_name
    subtitle = db.boards(request.args(0)).brd_desc
    #image = db.boards(request.args(0)).image
    id = request.args(0)
    totalmessages = len(messages)

    return dict(id=id, totalmessages=totalmessages, title=title, subtitle=subtitle)


def load_messages():
    """Loads all messages in the current board"""
    board_id = request.args(0)
    messages = db(db.messages.msg_brd == board_id).select()
    title = db.boards(board_id).brd_name
    subtitle = db.boards(board_id).brd_desc

    if isinstance(request.vars.page, str):
        page = int(request.vars.page)
    else:
        page = 0

    items_per_page = 4
    limitby = (page * items_per_page, (page + 1) * items_per_page)
    rows = db(db.messages.msg_brd == request.args(0)).select(db.messages.ALL, limitby=limitby, orderby=~db.messages.msg_time)

    d = []
    for r in rows:
        d.append({
            'id': r.id,
            'creator': r.creator,
            'creator_name': get_user_from_id(r.creator),
            'msg_time': r.msg_time,
            'image': r.image,
            'msg_title': r.msg_title,
            'msg_id': r.msg_id
        })
    msg_len = len(d)
    totalmessages = len(messages)
    logger.info("User %r, has requested %r messages from %r" % (auth.user_id, msg_len, title))
    return response.json(dict(user_id=auth.user_id, msg_dict=d, msg_len=msg_len, page=page, totalmessages=totalmessages, items_per_page=items_per_page))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
