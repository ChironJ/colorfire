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
    return static_file(filename, root='./static/')

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

def create_room(roomkey, number, datapath=CUSTOM_DATA_PATH):
    roominfo = {}
    roominfo['roomkey'] = roomkey
    roominfo['maxnum'] = number
    roominfo['usernum'] = 0
    roominfo['userinfo'] = {}
    roominfo['status'] = 0 #0正在进人 1游戏开始 2游戏结束
    roominfo['cardsinfo'] = {}
    roominfo['remindernum'] = 8
    roominfo['lightnum'] = 3
    f = open(datapath+"/"+roomkey, "w")
    f.write(json.dumps(roominfo, ensure_ascii=False)+"\n")
    f.close()
    return

def load_room(roomkey, datapath=CUSTOM_DATA_PATH):
    if not roomkey:
        return None
    f = open(datapath+"/"+roomkey, "r")
    inline = f.readline()
    f.close()
    return json.loads(inline)



def room_verify(func):
    '''
    定义一个装饰器用于装饰需要验证的页面
    装饰器必须放在route装饰器下面
    '''
    def wrapper(*args, **kwargs):
        roomkey = request.get_cookie('roomkey', secret="colorfire")
        print "room_verify:", roomkey
        print args, kwargs
        if not roomkey:
            return template('welcome.html')
        else:
            return func(*args,**kwargs)
    return wrapper


#进入房间
@mainapp.route('/room/<id:re:(\w+)>/')
def room(id):
    roomkey = request.get_cookie('roomkey', secret="colorfire")
    if roomkey != id:
        print "xx roomkey=", roomkey, "id=", id
        #print template("welcome.html")
        return template("welcome.html")
    roominfo = load_room(id)
    if not roominfo:
        return template("welcome.html")
    return roominfo



@mainapp.route('/load')
def load():
    roomkey = request.get_cookie('roomkey', secret="colorfire")
    str =  load_room(roomkey)
    print str
    return str


@mainapp.post('/createroom')
def createroom_submit():
    print "createroom_submit", request.headers.get('X-Requested-With')
    roomkey = request.forms.get('roomkey')#房间号
    response.set_cookie('roomkey', roomkey, secret="colorfire")
    #生成roomkey的文件
    number = request.forms.get('number')#房间人数
    create_room(roomkey, number)
    return redirect(request.script_name+'index')
    #return template('index.html', roomkey=roomkey)

@mainapp.get('/enterroom')
def enterroom_form():
    referer = request.get_header('Referer')
    if not referer:
        return redirect(request.script_name+'index')

    return template('enterroom.html')

@mainapp.post('/enterroom')
def enterroom_submit():
    return template('index.html')

@mainapp.route('/exit')
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
