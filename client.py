# coding=gbk
from socket import *
from select import *
from thread import *
from datetime import *
from random import *
import os
from time import *

input_buffers = ''
recv_buffers = ''

def login_process(conn_sock) :
    #print("call login_process")
    user_name = raw_input("请输入用户名:\n")
    password = raw_input("请输入密码:\n")
    conn_sock.send("login "+user_name+' '+password)

def create_process(conn_sock) :
    user_name = raw_input("请输入用户名:\n")
    password = raw_input("请输入密码:\n")
    confirm_password = raw_input("请再次输入密码:\n")
    conn_sock.send("create "+user_name+' '+password+' '+confirm_password)

def input_func(lock,port) :                  #因windows平台select不支持标准输入,所以用多线程实现。
    global recv_buffers
    host = '127.0.0.1'
    addr = (host,port)
    listen_sock = socket(AF_INET,SOCK_STREAM)
    listen_sock.bind(addr)
    listen_sock.listen(5)

    lock.release()
    conn_sock,addr= listen_sock.accept()
    listen_sock.close()
    
    none_command_input_msg(conn_sock)

    while True :
        if recv_buffers != '':
            handle_input_msg(recv_buffers,conn_sock)
            recv_buffers = ''


def command_hints() :
    print("本系统支持的命令及解释如下:")
    print("create_room roomname : 创建指定房间")
    print("enter_room roomname : 进入指定房间")
    print("quit_room : 离开房间")
    print("find_room : 查找当前所有房间")
    print("logout : 退出游戏大厅")
    print("chat username msg : 给指定用户发送消息")
    print("chat_lobby msg : 给游戏大厅里所有人发送消息")
    print("chat_room msg : 给房间里所有人发送消息")
    print("21game expression : 21点游戏的回答形式")

def game_msg(lists,conn_sock) :
        num1 = lists[1]
        num2 = lists[2]
        num3 = lists[3]
        num4 = lists[4]
        print("21点游戏开始")
        print("题目如下,你有30秒时间作答")
        print(int(num1),int(num2),int(num3),int(num4))
         

def handle_none_input_msg(data,conn_sock) :
    #print("handle_none_input_msg")
    if data.find("游戏胜利") != -1 :
        print(data)
        return
    lists = data.split('#')
    length = len(lists)
    if lists[0] == "21点游戏" :
        game_msg(lists,conn_sock)
        return
    if length != 2 :
        pass
    else :
        msg_type = lists[1]
        if msg_type == "私密消息" :
            #print("process private messgae")
            chat = lists[0]
            lst = chat.split(':')
            print("接收到来自%s的消息:%s" % (lst[0],lst[1]))
        elif msg_type == "房间消息" :
            chat = lists[0]
            lst = chat.split(':')
            print("接收到来自%s的房间消息:%s" % (lst[0],lst[1]))
        elif msg_type == "大厅消息" :
            chat = lists[0]
            lst = chat.split(':')
            print("接收到来自%s的大厅消息:%s" % (lst[0],lst[1]))

def input_msg(conn_sock) :
    data = raw_input()
    conn_sock.send(data)

def none_command_input_msg(conn_sock) :
    data = raw_input("输入1表示登录,输入2表示创建用户,输入3表示退出程序\n")
    if data == '1' :
        login_process(conn_sock)
    elif data == '2' :
        create_process(conn_sock)
    elif data == '3' :
        conn_sock.close()
        os._exit(0)
    else :
        conn_sock.send("无效的输入")                      

def handle_input_msg(data,conn_sock) :
    if data == "inner_use_inner" :
        input_msg(conn_sock)
        return
    lists = data.split('#')
    if lists[len(lists)-1] == "房间查找" :
        if len(lists) > 1 and lists[0] != '':
            print("房间的名字列表如下:")
            print(lists[0])
            input_msg(conn_sock)
            return
        else :
            print("当前还没有房间")
            input_msg(conn_sock)
            return
    data = lists[0]
    if data == "无效的用户" :
        print(data)
        none_command_input_msg(conn_sock)
    elif data == "请先登录" :
        print(data)
        none_command_input_msg(conn_sock)
    elif data == "登录成功" :
        print(data)
        command_hints()
        input_msg(conn_sock)
    elif data == "该用户已经在线" :
        print(data)
        none_command_input_msg(conn_sock)
    elif data == "恭喜你注册成功" :
        print(data)
        none_command_input_msg(conn_sock)
    elif data == "创建无效的命令" :
        print("非法的用户名或密码")
        none_command_input_msg(conn_sock)
    elif data == "该用户名已经被注册" :
        print(data)
        none_command_input_msg(conn_sock)
    elif data == "输入密码和上一次不一致" :
        print(data)
        none_command_input_msg(conn_sock)
    elif data == "用户名或密码错误" :
        print(data)
        none_command_input_msg(conn_sock)
    elif data == "成功创建房间" :
        print(data)
        input_msg(conn_sock)
    elif data == "处于房间中,无法创建新房间" :
        print(data)
        input_msg(conn_sock)
    elif data == "该房间已经被创建" :
        print(data)
        input_msg(conn_sock)
    elif data == "无法给无效的房间发送消息" :
        print("没有处于房间中")
        input_msg(conn_sock)
    elif data == "成功离开房间" :
        print(data)
        input_msg(conn_sock)
    elif data == "没有处于房间中,无法离开房间" :
        print(data)
        input_msg(conn_sock)
    elif data == "请先离开本房间,再加入其他房间" :
        print(data)
        input_msg(conn_sock)
    elif data == "无效的状态" :
        print(data)
        input_msg(conn_sock)
    elif data == "没有处理的状态" :
        print(data)
        input_msg(conn_sock)
    elif data == "成功进入房间" :
        print(data)
        input_msg(conn_sock)
    elif data == "无效的房间" :
        print(data)
        input_msg(conn_sock)
    elif data == "成功退出游戏大厅" :
        print(data)
        none_command_input_msg(conn_sock)
    elif data == "发送消息成功" :
        print(data)
        input_msg(conn_sock)
    elif data == "无法给无效的用户发送消息" :
        print(data)
        input_msg(conn_sock)
    elif data == "无效的命令" :
        print(data)
        command_hints()
        input_msg(conn_sock)
    elif data == "非法的算术表达式" :
        print(data)
        input_msg(conn_sock)
    elif data == "游戏在半点时间才会开始" :
        print(data)
        input_msg(conn_sock)
    elif data == "需要进入房间才能参与游戏" :
        print(data)
        input_msg(conn_sock)
    elif data == "服务器已经收到问题答案" :
        print("请等待游戏结果")
        input_msg(conn_sock)
    elif data == "恭喜你获得游戏胜利" :
        print(data)
        input_msg(conn_sock)
    elif data == "很遗憾未能获得游戏胜利" :
        print(data)
        input_msg(conn_sock)
    elif data == "没有在规定时间内作答" :
        print("游戏已经结束")
        input_msg(conn_sock)
    elif data == "游戏已经结束" :
        print(data)
        input_msg(conn_sock)
    elif data == "游戏还没有开始" :
        print(data)
        input_msg(conn_sock)
    elif data == "无效的输入" :
        print(data)
        none_command_input_msg(conn_sock)
    else :
        pass

            
def hash_func(num) :
    i = num
    total = 0
    while i != 0 :
        total += i % 10
        i /= 10
    return total

def client() :
    global recv_buffers
    global input_buffers
    port = randint(1,100000) % 20000 + 20000
    port = hash_func(port) + port
    lock = allocate_lock()
    lock.acquire()
    start_new_thread(input_func,(lock,port))

    while lock.locked() :
          pass
    host = '127.0.0.1'
    addr = (host,port)
    stdin_sock = socket(AF_INET,SOCK_STREAM)
    stdin_sock.connect(addr)
          
    host = '127.0.0.1'
    port = 12345
    bufsize = 4096
    addr = (host,port)
    conn_sock = socket(AF_INET,SOCK_STREAM)
    
    conn_sock.connect(addr)

    conn_fd = conn_sock.fileno()
    stdin_fd = stdin_sock.fileno()

    while True :
          r,w,e = [],[],[]

          r.append(conn_fd)
          r.append(stdin_fd)
          
          r,w,e = select(r,w,e)
           
          for fd in r :
              if fd == stdin_fd :
                  input_buffers = stdin_sock.recv(bufsize)
                  conn_sock.send(input_buffers)
              elif fd == conn_fd :
                  recv_buffers = conn_sock.recv(bufsize)
                  #print("recv message : %s" % recv_buffers)
                  if (recv_buffers.find("私密消息") != -1 or recv_buffers.find("房间消息") != -1 or
                      recv_buffers.find("大厅消息") != -1 or recv_buffers.find("游戏胜利") != -1) :
                      handle_none_input_msg(recv_buffers,conn_sock)
                      recv_buffers = 'inner_use_inner'
                  elif recv_buffers.find("21点游戏") != -1 :
                      handle_none_input_msg(recv_buffers,conn_sock)
                      recv_buffers = ''

          for fd in e :
            if fd == stdin_fd :
                stdin_sock.close()
            else :
                conn_sock.close()
                 
    
if __name__ == '__main__' :
    client()
    
         
    


          
