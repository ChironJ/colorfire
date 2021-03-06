#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys, os
import random
import string
import json
from bottle import static_file, Bottle
from bottle import jinja2_template as template
from bottle import request, response, redirect
from bottle import TEMPLATE_PATH
from settings import log

#获取当前文件夹的父目录绝对路径
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
#指定的模板路径
CUSTOM_TPL_PATH = BASE_DIR+"/views"
TEMPLATE_PATH.insert(0, CUSTOM_TPL_PATH)
#数据存放路径
CUSTOM_DATA_PATH = BASE_DIR+"/data"

reload(sys)
sys.setdefaultencoding('utf-8')
mainapp = Bottle()

#templates目录
#@mainapp.route('/templates/<filename:path>')
#def server_templates(filename):
#    return bottle.static_file(filename, root=CUSTOM_TPL_PATH)#绝对路径
@mainapp.route('/static/<filename:path>')
def server_static(filename):
    print "filename=", filename
    print os.path.dirname(__file__)
    print static_file(filename, root='./static/')
    return static_file(filename, root='./colorfire/static/')

def auth(func):
    '''
    定义一个装饰器用于装饰需要验证的页面
    装饰器必须放在route装饰器下面
    '''
    def wrapper(*args, **kwargs):
        roomkey = request.get_cookie('roomkey', secret="colorfire")
        print "author", roomkey
        print "author", request.headers.get('X-Requested-With')
        if not roomkey:
            return template('welcome.html')
        else:
            return func(*args,**kwargs)
    return wrapper



def create_room(roomkey, number):
    roominfo = {}
    roominfo['roomkey'] = roomkey
    roominfo['usermaxnum'] = number
    roominfo['usernum'] = 0
    roominfo['userinfo'] = {}

    roominfo['status'] = 0 #0正在进人 1游戏开始 2游戏结束
    roominfo['deck'] = {}
    roominfo['deadwood'] = {}
    roominfo['deskinfo'] = {}
    for color in ['r','g','b','y','w']:
        roominfo['deskinfo'][color] = 0
        roominfo['deck'][color] = {"1":3,"2":2,"3":2,"4":2,"5":1}
        roominfo['deadwood'][color] = {"1":0,"2":0,"3":0,"4":0,"5":0}
    roominfo['remindernum'] = 8
    roominfo['remindermaxnum'] = 8
    roominfo['lightnum'] = 3
    return roominfo

def add_room_user(roominfo, username):
    if 'userinfo' not in roominfo or \
        'usernum' not in roominfo or \
        'usermaxnum' not in roominfo:
        return False
    if username not in roominfo['userinfo'] and \
        roominfo['usernum'] < roominfo['usermaxnum']:
        info = {}
        info['name'] = username
        roominfo[username] = 

        roominfo['userinfo']

def save_room(roomkey, roominfo, datapath=CUSTOM_DATA_PATH):
    if not roomkey:
        return None
    f = open(datapath+"/"+roomkey, "w")
    f.write(json.dumps(roominfo, ensure_ascii=False)+"\n")
    f.close()
    return

def load_room(roomkey, datapath=CUSTOM_DATA_PATH):
    if not roomkey:
        return None
    f = open(datapath+"/"+roomkey, "r")
    inline = f.readline()
    roominfo = json.loads(inline)
    f.close()
    return roominfo

def room_verify(func):
    def handle_args(id, *args, **kwargs):
        roomkey = request.get_cookie('roomkey', secret="colorfire")
        log.info('[room_verify][roomkey='+roomkey+'][id='+id+']')
        print "room_verify:", roomkey, id
        valid = False
        if roomkey == id:
            valid = True
        if not valid:
            return template('welcome.html')
        return func(id, *args, **kwargs)
    return handle_args



#进入房间
@mainapp.route('/room/<id:re:(\w+)>')
@room_verify
def room(id):
    roominfo = load_room(id)

        user_list = [{"name":"用户一"},{"name":"用户二"},{}]
    return template("room.html")


@mainapp.route('/load')
def load():
    roomkey = request.get_cookie('roomkey', secret="colorfire")
    str =  load_room(roomkey)
    print str
    return str

@mainapp.get('/createroom')
def createroom_form():
    #print request.headers.keys() #查看所有header key
    referer = request.get_header('Referer')
    print "createroom", referer
    if not referer or referer.rsplit('/', 1) == 'createroom':
        #print request.fullpath #查看url的全路径
        return redirect(request.script_name+'index')
    roomkey = "".join(random.sample('zyxwvutsrqponmlkjihgfedcba',5))
    return template('createroom.html', locals())

@mainapp.post('/createroom')
def createroom_submit():
    print "createroom_submit", request.headers.get('X-Requested-With')
    roomkey = request.forms.get('roomkey')#房间号
    response.set_cookie('roomkey', roomkey, secret="colorfire")
    #生成roomkey的文件
    number = request.forms.get('number')#房间人数
    create_room(roomkey, number)
    return redirect(request.script_name+'room/'+roomkey)
    #return redirect(request.script_name+'index')

@mainapp.get('/enterroom')
def enterroom_form():
    referer = request.get_header('Referer')
    if not referer:
        return redirect(request.script_name+'index')

    return template('enterroom.html')

@mainapp.post('/enterroom')
def enterroom_submit():
    return template('index.html')

@mainapp.route('/exitroom')
def exit():
    response.delete_cookie('roomkey')
    return redirect(request.script_name+'index')

@mainapp.route('/random')
def rand():
    r = random.randint(12, 20)
    print r
    return r

@mainapp.get('/index')
@mainapp.get('/')
@auth
def index():
    print "index", request.headers.get('X-Requested-With')
    print "index", request.cookies.keys(), request.cookies.values()
    roomkey = request.get_cookie('roomkey', secret="colorfire")
    user_list = [{"name":"用户一"},{"name":"用户二"},{}]
    #print template('index.html', locals())
    return template('index.html', locals())
