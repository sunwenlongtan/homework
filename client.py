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
    user_name = raw_input("�������û���:\n")
    password = raw_input("����������:\n")
    conn_sock.send("login "+user_name+' '+password)

def create_process(conn_sock) :
    user_name = raw_input("�������û���:\n")
    password = raw_input("����������:\n")
    confirm_password = raw_input("���ٴ���������:\n")
    conn_sock.send("create "+user_name+' '+password+' '+confirm_password)

def input_func(lock,port) :                  #��windowsƽ̨select��֧�ֱ�׼����,�����ö��߳�ʵ�֡�
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
    print("��ϵͳ֧�ֵ������������:")
    print("create_room roomname : ����ָ������")
    print("enter_room roomname : ����ָ������")
    print("quit_room : �뿪����")
    print("find_room : ���ҵ�ǰ���з���")
    print("logout : �˳���Ϸ����")
    print("chat username msg : ��ָ���û�������Ϣ")
    print("chat_lobby msg : ����Ϸ�����������˷�����Ϣ")
    print("chat_room msg : �������������˷�����Ϣ")
    print("21game expression : 21����Ϸ�Ļش���ʽ")

def game_msg(lists,conn_sock) :
        num1 = lists[1]
        num2 = lists[2]
        num3 = lists[3]
        num4 = lists[4]
        print("21����Ϸ��ʼ")
        print("��Ŀ����,����30��ʱ������")
        print(int(num1),int(num2),int(num3),int(num4))
         

def handle_none_input_msg(data,conn_sock) :
    #print("handle_none_input_msg")
    if data.find("��Ϸʤ��") != -1 :
        print(data)
        return
    lists = data.split('#')
    length = len(lists)
    if lists[0] == "21����Ϸ" :
        game_msg(lists,conn_sock)
        return
    if length != 2 :
        pass
    else :
        msg_type = lists[1]
        if msg_type == "˽����Ϣ" :
            #print("process private messgae")
            chat = lists[0]
            lst = chat.split(':')
            print("���յ�����%s����Ϣ:%s" % (lst[0],lst[1]))
        elif msg_type == "������Ϣ" :
            chat = lists[0]
            lst = chat.split(':')
            print("���յ�����%s�ķ�����Ϣ:%s" % (lst[0],lst[1]))
        elif msg_type == "������Ϣ" :
            chat = lists[0]
            lst = chat.split(':')
            print("���յ�����%s�Ĵ�����Ϣ:%s" % (lst[0],lst[1]))

def input_msg(conn_sock) :
    data = raw_input()
    conn_sock.send(data)

def none_command_input_msg(conn_sock) :
    data = raw_input("����1��ʾ��¼,����2��ʾ�����û�,����3��ʾ�˳�����\n")
    if data == '1' :
        login_process(conn_sock)
    elif data == '2' :
        create_process(conn_sock)
    elif data == '3' :
        conn_sock.close()
        os._exit(0)
    else :
        conn_sock.send("��Ч������")                      

def handle_input_msg(data,conn_sock) :
    if data == "inner_use_inner" :
        input_msg(conn_sock)
        return
    lists = data.split('#')
    if lists[len(lists)-1] == "�������" :
        if len(lists) > 1 and lists[0] != '':
            print("����������б�����:")
            print(lists[0])
            input_msg(conn_sock)
            return
        else :
            print("��ǰ��û�з���")
            input_msg(conn_sock)
            return
    data = lists[0]
    if data == "��Ч���û�" :
        print(data)
        none_command_input_msg(conn_sock)
    elif data == "���ȵ�¼" :
        print(data)
        none_command_input_msg(conn_sock)
    elif data == "��¼�ɹ�" :
        print(data)
        command_hints()
        input_msg(conn_sock)
    elif data == "���û��Ѿ�����" :
        print(data)
        none_command_input_msg(conn_sock)
    elif data == "��ϲ��ע��ɹ�" :
        print(data)
        none_command_input_msg(conn_sock)
    elif data == "������Ч������" :
        print("�Ƿ����û���������")
        none_command_input_msg(conn_sock)
    elif data == "���û����Ѿ���ע��" :
        print(data)
        none_command_input_msg(conn_sock)
    elif data == "�����������һ�β�һ��" :
        print(data)
        none_command_input_msg(conn_sock)
    elif data == "�û������������" :
        print(data)
        none_command_input_msg(conn_sock)
    elif data == "�ɹ���������" :
        print(data)
        input_msg(conn_sock)
    elif data == "���ڷ�����,�޷������·���" :
        print(data)
        input_msg(conn_sock)
    elif data == "�÷����Ѿ�������" :
        print(data)
        input_msg(conn_sock)
    elif data == "�޷�����Ч�ķ��䷢����Ϣ" :
        print("û�д��ڷ�����")
        input_msg(conn_sock)
    elif data == "�ɹ��뿪����" :
        print(data)
        input_msg(conn_sock)
    elif data == "û�д��ڷ�����,�޷��뿪����" :
        print(data)
        input_msg(conn_sock)
    elif data == "�����뿪������,�ټ�����������" :
        print(data)
        input_msg(conn_sock)
    elif data == "��Ч��״̬" :
        print(data)
        input_msg(conn_sock)
    elif data == "û�д����״̬" :
        print(data)
        input_msg(conn_sock)
    elif data == "�ɹ����뷿��" :
        print(data)
        input_msg(conn_sock)
    elif data == "��Ч�ķ���" :
        print(data)
        input_msg(conn_sock)
    elif data == "�ɹ��˳���Ϸ����" :
        print(data)
        none_command_input_msg(conn_sock)
    elif data == "������Ϣ�ɹ�" :
        print(data)
        input_msg(conn_sock)
    elif data == "�޷�����Ч���û�������Ϣ" :
        print(data)
        input_msg(conn_sock)
    elif data == "��Ч������" :
        print(data)
        command_hints()
        input_msg(conn_sock)
    elif data == "�Ƿ����������ʽ" :
        print(data)
        input_msg(conn_sock)
    elif data == "��Ϸ�ڰ��ʱ��ŻῪʼ" :
        print(data)
        input_msg(conn_sock)
    elif data == "��Ҫ���뷿����ܲ�����Ϸ" :
        print(data)
        input_msg(conn_sock)
    elif data == "�������Ѿ��յ������" :
        print("��ȴ���Ϸ���")
        input_msg(conn_sock)
    elif data == "��ϲ������Ϸʤ��" :
        print(data)
        input_msg(conn_sock)
    elif data == "���ź�δ�ܻ����Ϸʤ��" :
        print(data)
        input_msg(conn_sock)
    elif data == "û���ڹ涨ʱ��������" :
        print("��Ϸ�Ѿ�����")
        input_msg(conn_sock)
    elif data == "��Ϸ�Ѿ�����" :
        print(data)
        input_msg(conn_sock)
    elif data == "��Ϸ��û�п�ʼ" :
        print(data)
        input_msg(conn_sock)
    elif data == "��Ч������" :
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
                  if (recv_buffers.find("˽����Ϣ") != -1 or recv_buffers.find("������Ϣ") != -1 or
                      recv_buffers.find("������Ϣ") != -1 or recv_buffers.find("��Ϸʤ��") != -1) :
                      handle_none_input_msg(recv_buffers,conn_sock)
                      recv_buffers = 'inner_use_inner'
                  elif recv_buffers.find("21����Ϸ") != -1 :
                      handle_none_input_msg(recv_buffers,conn_sock)
                      recv_buffers = ''

          for fd in e :
            if fd == stdin_fd :
                stdin_sock.close()
            else :
                conn_sock.close()
                 
    
if __name__ == '__main__' :
    client()
    
         
    


          
