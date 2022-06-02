from tkinter import *
# Client
from socket import *
from threading import *
import os
import datetime
import time
#--------------클라이언트 세팅 -----------------------
Host='127.0.0.1' # 서버의 IP주소를 입력하세요.
Port = 2021 # 사용할 포트 번호. 
#---------------------------------------
    
def now_time(): 
    now = datetime.datetime.now()
    time_str=now.strftime('[%H:%M] ')
    return time_str
​
def send_func():
    global client_sock
    send_data=(message_input.get(1.0, "end")).rstrip()
    client_sock.send(send_data.encode('utf-8'))
    chat_log['state'] = 'normal'
    chat_log.insert("end",'\n' + now_time() + send_data)
    chat_log['state'] = 'disabled'
    message_input.delete(1.0, "end")
​
def recv_func():
    global client_sock
    while True:
        try:
            recv_data=(client_sock.recv(1024)).decode('utf-8')
            if len(recv_data)==0:
                chat_log['state'] = 'normal'
                chat_log.insert("end",'\n' + '[공지] 서버와의 연결이 끊어졌습니다.')
                chat_log['state'] = 'disabled'
                client_sock.close()
                os._exit(1)
        except Exception as e:
            chat_log['state'] = 'normal'
            chat_log.insert("end",'\n' + '예외가 발생했습니다.' + e)
            chat_log.insert("end",'\n' + '[공지] 메시지를 수신하지 못하였습니다.')
            chat_log['state'] = 'disabled'
            client_sock.close()
            os._exit(1)
        else:
            chat_log['state'] = 'normal'
            chat_log.insert("end",'\n' + recv_data)
            chat_log['state'] = 'disabled'
            pass
​
def login():
    global client_sock
    i = 0
    login_button['state'] = 'disabled'
    logout_button['state'] = 'active'
    ip_entry['state'] = 'readonly'
    port_entry['state'] = 'readonly'
    Host = ip_entry.get(); Port = int(port_entry.get())
    client_sock=socket(AF_INET, SOCK_STREAM)
    try:
        client_sock.connect((Host,Port))
    except ConnectionRefusedError:
        chat_log['state'] = 'normal'
        chat_log.insert("end",'\n' + '서버에 연결할 수 없습니다.')
        chat_log.insert("end",'\n' + '1. 서버의 ip주소와 포트번호가 올바른지 확인하십시오.')
        chat_log.insert("end",'\n' + '2. 서버 실행 여부를 확인하십시오.')
        chat_log['state'] = 'disabled'
        client_sock.close()
        return
​
    except:
        chat_log['state'] = 'normal'
        chat_log.insert("end",'\n' + '프로그램을 정상적으로 실행할 수 없습니다.')
        chat_log['state'] = 'disable'
        client_sock.close()
        return
    else:
        chat_log['state'] = 'normal'
        chat_log.insert("end",'\n' + '[공지] 서버와 연결되었습니다.')
        name = nick_entry.get();
    while True:
        if ' ' in name:
            chat_log.insert("end",'\n' + '공백은 입력이 불가능합니다.')
            i = i + 1
            name = "guest" + str(i)
            continue
        client_sock.send(name.encode())
        is_possible_name=client_sock.recv(1024).decode()
​
        if is_possible_name=='yes':
            chat_log['state'] = 'normal'
            chat_log.insert("end",'\n' + '채팅방에 입장하였습니다.')
            client_sock.send('!enter'.encode())
            break
            
        elif is_possible_name=='overlapped':
            chat_log.insert("end",'\n' + '[공지] 이미 사용중인 닉네임입니다.')
            i = i + 1
            name = "guest" + str(i)
            continue
        elif len(client_sock.recv(1024).decode())==0:
            chat_log.insert("end",'\n' + '[공지] 서버와의 연결이 끊어졌습니다.')
            client_sock.close()
            return
    sender=Thread(target=send_func, args=())
    receiver=Thread(target=recv_func, args=())
    sender.start()
    receiver.start()
​
    
def logout():
    login_button['state'] = 'active'
    logout_button['state'] = 'disabled'
    ip_entry['state'] = 'normal'
    port_entry['state'] = 'normal'
    send_data = '!quit'
    client_sock.send(send_data.encode('utf-8'))
    client_sock.close()
    
client_sock=socket(AF_INET, SOCK_STREAM)
window = Tk()
window.title('채팅 프로그램: client')
window.geometry("700x500")
window.resizable(False, False)
​
Label(window, text = 'Server IP : ').place(x=20, y=20)
Label(window, text = 'Port : ').place(x=200, y=20)
Label(window, text = 'Nickname : ').place(x=300, y=20)
ip_entry = Entry(window, width=14); ip_entry.place(x=80, y=21)
ip_entry.insert(0,Host)
port_entry = Entry(window, width=5); port_entry.place(x = 235, y=21)
port_entry.insert(0, Port)
nick_entry = Entry(window, width = 14); nick_entry.place(x=370, y=21)
nick_entry.insert(0, 'team10')
​
login_button = Button(window,text='login', command=login); login_button.place(x=580, y=18)
logout_button = Button(window,text='logout',state = 'disabled', command = logout); logout_button.place(x=630, y=18)
​
​
chat_frame = Frame(window)
chat_log = Text(chat_frame, width = 92, height = 24, state = 'disabled') ; chat_log.pack(side='left')
chat_frame.place(x=20, y=60)
message_input = Text(window, width = 85, height = 4) ; message_input.place(x=20,y = 390)
send_button = Button(window, text = 'Send', command = lambda:send_func()); send_button.place(x=630, y=405)
​
sender=Thread(target=send_func, args=())
receiver=Thread(target=recv_func, args=())
sender.start()
receiver.start()
​
window.mainloop()
​
