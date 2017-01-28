# coding=gbk
from socket import *
from select import *
from string import *
from thread import *
from random import *
from datetime import *
from time import *

class Client(object):
    def __init__(self) :
        self.name = ''  #用户名
        self.time = 0    #在线时长
        self.state = False #是否在线
        self.room = ''  #房间名
        self.owner = False #是否为房主
        self.enter_room_time = ''
        self.msg = ''   #消息
        self.begin = False  #游戏是否开始
        self.first = True  #是否首次开始游戏
        self.res = ''      #游戏答案
        self.ans_time = ''  #回答游戏时间
        

class Room(object):
    def __init__(self, name, owner, members):
        self.name = name
        self.owner = owner
        self.members = members
        self.state = False

def load_file(database) :
        f = open(database,'r')
        users = {}
        while True :
            data = f.readline();
            if not data :
                break
            if data == '\n' :
                continue
            user_name,password,time = data.split(' ')
            users[user_name] = [password,time]
        f.close()
        return users

def save_file(users,database) :
    f = open(database,'w')
    for user in users.keys() :
        user_name = user
        password = users[user][0]
        time = users[user][1]
        f.write(user_name+' '+password+' '+time+'\n')
    f.close()

def create_process(data,database) :
    try :
        user_name,password,confirm_password = data.split(' ')

        if password != confirm_password :
            return '输入密码和上一次不一致'

        users = load_file(database)

        for user in users.keys() :
            if user == user_name :
                return '该用户名已经被注册'

        users[user_name] = [password,'0']

        save_file(users,database)

        return '恭喜你注册成功'
    except :
        return "创建无效的命令"

def login_process(fd,data,database,clientset) :
    #print("in login_process")
    try :   
        user_name,password = data.split(' ')
        for item in clientset :
            if clientset[item].name == user_name :
                return "该用户已经在线"
        users = load_file(database)
        for user in users.keys() :
            if user == user_name and users[user][0] == password :
                client = Client()
                client.name = user_name
                client.time = datetime.now()
                client.state = True
                clientset[fd] = client
                return '登录成功'
        return '用户名或密码错误'
    except :
        return '用户名或密码错误'

def create_room_process(fd,data,rooms,clientset) :
    try :
        name = data
        for r in rooms:
            if r.name == name:
                return '该房间已经被创建'
        if clientset[fd].room!= '':
            return '处于房间中,无法创建新房间'
        room = Room(name,clientset[fd].name,[clientset[fd].name])
        clientset[fd].room = room
        clientset[fd].owner = True
        clientset[fd].enter_room_time = datetime.now()
        rooms.append(room)
        return '成功创建房间'
    except :
        return "无效的命令"

def enter_room_process(fd,data,rooms,clientset) :
    try :
        name = data
    
        if clientset[fd].room != '' :
            return '请先离开本房间,再加入其他房间'
        for r in rooms :
            if r.name == name :
                r.members.append(clientset[fd].name)
                clientset[fd].room = r
                clientset[fd].enter_room_time = datetime.now()
                return '成功进入房间'
            
        return '无效的房间'
    except :
        return "无效的命令"

def quit_room_process(fd,rooms,clientset) :
    try :
        if clientset[fd].room == '':
            return '没有处于房间中,无法离开房间'
        r = clientset[fd].room
        if clientset[fd].owner == True :
            tmp = r
            clientset[fd].room = ''
            clientset[fd].owner = False
            clientset[fd].enter_room_time = ''
            clientset[fd].begin = False
            clientset[fd].first = True
            clientset[fd].res = ''
            clientset[fd].ans_time = ''
            if len(tmp.members) == 1:
                rooms.remove(r)
            elif len(tmp.members) > 1 :
                tmp.members.remove(clientset[fd].name)
                user_name = tmp.members[0]
                user = ''
                for i in clientset :
                    if clientset[i].name == user_name :
                        user = clientset[i]
                        break
                user.owner = True
                rooms.remove(r)
                rooms.append(tmp)
            return '成功离开房间'
        else :
            r = clientset[fd].room
            clientset[fd].room = ''
            clientset[fd].enter_room_time = ''
            clientset[fd].begin = False
            clientset[fd].first = True
            clientset[fd].res = ''
            clientset[fd].ans_time = ''
            tmp = r
            tmp.members.remove(clientset[fd].name)
            rooms.remove(r)
            rooms.append(tmp)
            return '成功离开房间'
        return '无效的状态'
    except :
        return "无效的命令"

def find_room_process(rooms) :
        res = []
        for r in rooms :
            res.append(r.name)
        return res

def logout_process(fd,database,rooms,clientset) :
    try :
        if fd not in clientset :
            return "没有登录"
        users = load_file(database)
        for user in users.keys() :
            if user == clientset[fd].name :
                time = datetime.now()
                delt = time - clientset[fd].time
                num = int(users[user][1])
                num += delt.seconds
                users[user][1] = str(num)
                break
        save_file(users,database)
        if clientset[fd].room == '' :
            clientset[fd].state = False
            clientset[fd].time = 0
            clientset[fd].name = ''
            clientset[fd].room = ''
            clientset[fd].owner = False
            clientset[fd].enter_room_time = ''
            clientset[fd].begin = False
            clientset[fd].first = True
            clientset[fd].res = ''
            clientset[fd].ans_time = ''
            return '成功退出游戏大厅'

        if clientset[fd].owner == True :
            r = clientset[fd].room
            tmp = r
            if len(tmp.members) == 1:
                rooms.remove(r)
            elif len(tmp.members) > 1 :
                tmp.members.remove(clientset[fd].name)
                user_name = tmp.members[0]
                user = ''
                for i in clientset :
                    if clientset[i].name == user_name :
                        user = clientset[i]
                        break
                user.owner = True
                rooms.remove(r)
                rooms.append(tmp)
            clientset[fd].name = ''
            clientset[fd].time = 0
            clientset[fd].state = False
            clientset[fd].room = ''
            clientset[fd].owner = False
            clientset[fd].enter_room_time = ''
            clientset[fd].begin = False
            clientset[fd].first = True
            clientset[fd].res = ''
            clientset[fd].ans_time = ''
            clientset[fd].room = ''
            return '成功退出游戏大厅'
        else :
            r = clientset[fd].room
            tmp = r
            tmp.members.remove(clientset[fd].name)
            rooms.remove(r)
            rooms.append(tmp)
            clientset[fd].state = False
            clientset[fd].time = 0
            clientset[fd].name = ''
            clientset[fd].room = ''
            clientset[fd].owner = False
            clientset[fd].enter_room_time = ''
            clientset[fd].begin = False
            clientset[fd].first = True
            clientset[fd].res = ''
            clientset[fd].ans_time = ''
            clientset[fd].room = ''
            return '成功退出游戏大厅'
        return '无效的状态'
    except :
        return "无效的命令"

def chat_process(fd,data,clientset,sockset) :
    try :
        #print("in chat_process")
        my = clientset[fd].name + ':'
        lists = data.split(' ')
        name = lists[0]
        chat = ''
        for i in range(1, len(lists)):
            chat += lists[i] + ' '
        chat = my + chat
        other = None
        for item in clientset :
            if clientset[item].name == name :
                other = sockset[item]
        if other is None:
            return "无法给无效的用户发送消息"
        other.send(chat+"#私密消息")
        return "发送消息成功"
    except :
        return "无效的命令"

def chat_room_process(fd,data,rooms,clientset,sockset) :
    try :
        #print("in chat_room_process")
        my = clientset[fd].name + ':'
        chat = my + data
        r = clientset[fd].room
        if r == '' :
            return "无法给无效的房间发送消息"
        for item in clientset :
            if clientset[item].room == clientset[fd].room and item != fd :
                conn_sock = sockset[item]
                conn_sock.send(chat+"#房间消息")
        return "发送消息成功"
    except :
        return "无效的命令"

def chat_lobby_process(fd,data,clientset,sockset) :
    try :
        #print("in chat_lobby_process")
        if clientset[fd].name == '' :
            return "请先登录"
        my = clientset[fd].name + ':'
        chat = my + data
        for item in clientset :
            if item != fd :
                conn_sock = sockset[item]
                conn_sock.send(chat+"#大厅消息")

        return "发送消息成功"
    except :
        return "无效的命令"

def game_process(fd,data,clientset,sockset) :
    try :
        global num1,num2,num3,num4
        if clientset[fd].room == '' :
            return "需要进入房间才能参与游戏"
        current = datetime.now()
        '''if current.minute != 30 and current.minute != 0 :
            return "游戏在半点时间才会开始"'''
        if clientset[fd].begin == False and clientset[fd].first == True :
            return "游戏还没有开始"
        elif clientset[fd].begin == False and clientset[fd].first == False :
            return "游戏已经结束"
        delt = datetime.now() - clientset[fd].ans_time
    
        if delt.seconds <= 30 :
            try :
                if (data.find(str(num1)) != -1 and data.find(str(num2)) != -1 and
                   data.find(str(num3)) != -1 and data.find(str(num4)) != -1) :
                    clientset[fd].res = [eval(data),int(delt.seconds)]
                    return "服务器已经收到问题答案"
                else :
                    clientset[fd].res = [1234,1234]
                    return "非法的算术表达式" 
            except :
                return "非法的算术表达式"
        else :
            return "没有在规定时间内作答"
    except :
        return "无效的命令"
        

def other_command_process(fd,data,database,rooms,clientset,sockset) :
    try :
        if data == "无效的输入" :
            return data
        cmd,msg = '',''
        if data == "quit_room" or data == "logout" or data == "find_room" :
            cmd,msg = data,None
        else :
            lists = data.split(' ')
            cmd = lists[0]
            for item in range(1,len(lists)) :
                msg += (lists[item]+' ') 
        if cmd == "create_room" :
            if not msg :
                return "无效的命令"
            res = create_room_process(fd,msg,rooms,clientset)
        elif cmd == "enter_room" :
            if not msg :
                return "无效的命令"
            res = enter_room_process(fd,msg,rooms,clientset)
        elif cmd == "quit_room" :
            if msg :
                return "无效的命令"
            res = quit_room_process(fd,rooms,clientset)
        elif cmd == "find_room" :
            res = find_room_process(rooms)
        elif cmd == "logout" :
            res = logout_process(fd,database,rooms,clientset)
        elif cmd == "chat" :
            res = chat_process(fd,msg,clientset,sockset)
        elif cmd == "chat_lobby" :
            res = chat_lobby_process(fd,msg,clientset,sockset)
        elif cmd == "chat_room" :
            res = chat_room_process(fd,msg,rooms,clientset,sockset)
        elif cmd == "21game" :
            res = game_process(fd,msg,clientset,sockset)
        else :
            res = "无效的命令"
        return res
    except :
        return "无效的命令"

def handle_msg(sock,data,database,rooms,clientset,sockset) :
    index = data.find(' ')
    cmd = data[:index]
    msg = data[index+1:]
    res = ''
    if cmd == 'login' :
        #print("in handle_msg process login")
        res = login_process(sock.fileno(),msg,database,clientset)
    elif cmd == 'create' :
        res = create_process(msg,database)
    else :
        res = other_command_process(sock.fileno(),data,database,rooms,clientset,sockset)
    return res

def send_msg(sock,data) :
    if type(data) == type([]) :
        ans = ''
        for item in data :
            ans += (item + '\n')
        length = len(ans)
        if length == 0 :
            ans += "#房间查找"
        else :
            ans = ans[:length-1]
            ans += "#房间查找"
        sock.send(ans)
    else :
        sock.send(data)

num1 = ''
num2 = ''
num3 = ''
num4 = ''

def thread_game_process(clientset,sockset) :
    global num1,num2,num3,num4
    while True :
        #print("in thread_game_process while loop")
        current = datetime.now()
        hash_set = {}
        #if current.minute == 30 or current.minute == 0 :
        if current.minute < 60 and current.minute >= 0:
            for item in clientset :
                if clientset[item].room != '' :
                    clientset[item].begin = True
                    if clientset[item].room not in hash_set :
                        hash_set[clientset[item].room] = []
                    hash_set[clientset[item].room].append(item)
            num1 = randint(1,10)
            num2 = randint(1,10)
            num3 = randint(1,10)
            num4 = randint(1,10)
            for item in hash_set :
                lst = hash_set[item]
                for i in lst :
                    conn_sock = sockset[i]
                    conn_sock.send("21点游戏#"+str(num1)+'#'+str(num2)+
                                   '#'+str(num3)+'#'+str(num4))
                    clientset[i].ans_time = datetime.now()
                    clientset[i].first = False

            '''while (datetime.now() - current).seconds != 30 :
                pass'''

            sleep(30.0)

            hash_set.clear()
            
            for item in clientset :
                if clientset[item].room != '' and (datetime.now() - clientset[item].enter_room_time).seconds >= 30:
                    clientset[item].begin = True
                    if clientset[item].room not in hash_set :
                        hash_set[clientset[item].room] = []
                    hash_set[clientset[item].room].append(item)
                    
            for item in hash_set :
                lst = hash_set[item]
                hash_res = {}
                for i in lst :
                    if clientset[i].res != '' :
                        res = int(clientset[i].res[0])
                        hash_res[res] = i
                keys = hash_res.keys()
                keys.sort()
                keys.reverse()
                time = {}
                for key in keys :
                    if key == 21 :
                        time[clientset[hash_res[key]].res[1]] = hash_res[key]

                #print("here")

                if len(time) > 0 :
                    keys = time.keys()
                    keys.sort()
                    conn_sock = sockset[time[keys[0]]]
                    conn_sock.send("恭喜你获得游戏胜利")
                    clientset[time[keys[0]]].res = ''
                    clientset[time[keys[0]]].ans_time = ''
                    clientset[time[keys[0]]].begin = False
                        
                    for i in lst :
                        if i != time[keys[0]] :
                            conn_sock = sockset[i]
                            clientset[i].res = ''
                            clientset[i].ans_time = ''
                            clientset[i].begin = False
                            conn_sock.send("很遗憾未能获得游戏胜利")
                else :
                    only = ''
                    for key in keys :
                        if key <= 21 :
                            conn_sock = sockset[hash_res[key]]
                            only = hash_res[key]
                            clientset[only].res = ''
                            clientset[only].ans_time = ''
                            clientset[only].begin = False
                            conn_sock.send("恭喜你获得游戏胜利")
                            break

                    for i in lst :
                        if i != only :
                            conn_sock = sockset[i]
                            clientset[i].res = ''
                            clientset[i].ans_time = ''
                            clientset[i].begin = False
                            conn_sock.send("很遗憾未能获得游戏胜利")
        sleep(60.0)


def server(database) :
    host = '127.0.0.1'
    port = 12345
    addr = (host,port)
    listen_sock = socket(AF_INET,SOCK_STREAM)
    #listen_sock.bind((gethostname(),12345))
    listen_sock.bind(addr)
    listen_sock.listen(5)

    bufsize = 4096
    sockset = {}
    clientset = {}
    rooms = []
    listen_fd = listen_sock.fileno()
    sockset[listen_fd] = listen_sock

    start_new_thread(thread_game_process,(clientset,sockset))

    while True :
        r,w,e = [],[],[]
        
        for fd in sockset :
            r.append(fd)
            e.append(fd)
            
        r,w,e = select(r,w,e)
        
        for fd in r :
            sock = sockset[fd]
            
            if fd == listen_fd :
                conn_sock,cli_addr = sock.accept()
                conn_fd = conn_sock.fileno()
                sockset[conn_fd] = conn_sock
            else :
                try : 
                    data = sock.recv(bufsize)
                except IOError as e:
                    sock.close()
                    del sockset[fd]
                    if fd in clientset :
                        logout_process(fd,database,rooms,clientset)
                        del clientset[fd]
                else :
                    res = handle_msg(sock,data,database,rooms,clientset,sockset)
                    send_msg(sock,res)
                
        for fd in e :
            if fd in sockset :
                sock = sockset[fd]
                sock.close()
                del sockset[fd]
                if fd in clientset :
                    logout_process(fd,database,rooms,clientset)
                    del clientset[fd]

if __name__ == '__main__' :
    server("data.txt")
