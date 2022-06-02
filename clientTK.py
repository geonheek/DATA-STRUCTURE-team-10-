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
​
​
    
def now_time(): 
    now = datetime.datetime.now()
    time_str=now.strftime('[%H:%M] ')
    return time_str
def send_func():
    send_data=(message_input.get(1.0, "end")).rstrip()
    client_sock.send(send_data.encode('utf-8'))
    chat_log['state'] = 'normal'
    chat_log.insert("end",'\n' + now_time() + send_data)
    chat_log['state'] = 'disabled'
    if send_data=='!quit':
        print('연결을 종료하였습니다.')
        client_sock.close()
        os._exit(1)
    message_input.delete(1.0, "end")
def recv_func():
    while True:
        try:
            recv_data=(client_sock.recv(1024)).decode('utf-8')
            if len(recv_data)==0:
                print('[공지] 서버와의 연결이 끊어졌습니다.')
                client_sock.close()
                os._exit(1)
        except Exception as e:
            print('예외가 발생했습니다.', e) # 예외처리중
            print('[공지] 메시지를 수신하지 못하였습니다.')
        else:
            chat_log['state'] = 'normal'
            chat_log.insert("end",'\n' + recv_data)
            chat_log['state'] = 'disabled'
            pass
​
# 로그인 로그아웃 구현하면 login 함수로 옯겨야 하는 코드
client_sock=socket(AF_INET, SOCK_STREAM)
try:
    client_sock.connect((Host,Port))
except ConnectionRefusedError:
    print('서버에 연결할 수 없습니다.')
    print('1. 서버의 ip주소와 포트번호가 올바른지 확인하십시오.')
    print('2. 서버 실행 여부를 확인하십시오.')
    os._exit(1)
except:
    print('프로그램을 정상적으로 실행할 수 없습니다.')
else:
    print('[공지] 서버와 연결되었습니다.')
while True:
    name = input('사용하실 닉네임을 입력하세요 :')     
    if ' ' in name:
        print('공백은 입력이 불가능합니다.')
        continue
    client_sock.send(name.encode())
    is_possible_name=client_sock.recv(1024).decode()
    
    if is_possible_name=='yes':
        print(now_time()+ '채팅방에 입장하였습니다.')
        client_sock.send('!enter'.encode())
        break
    elif is_possible_name=='overlapped':
        print('[공지] 이미 사용중인 닉네임입니다.')
    elif len(client_sock.recv(1024).decode())==0:
        print('[공지] 서버와의 연결이 끊어졌습니다.')
        client_sock.close()
        os._exit(1)
​
​
# tkinter 적용 부분, send, recv의 정상작동 처리 부분도 tkinter 적용 완료 
window = Tk()
window.title('채팅 프로그램: client')
window.geometry("500x500")
window.resizable(False, False)
​
Label(window, text = 'Server IP : ').place(x=20, y=20)
Label(window, text = 'Port : ').place(x=250, y=20)
ip_entry = Entry(window, width=14); ip_entry.place(x=83, y=21)
ip_entry.insert(0,Host)
port_entry = Entry(window, width=5); port_entry.place(x = 290, y=21)
port_entry.insert(0, Port)
​
chat_frame = Frame(window)
chat_log = Text(chat_frame, width = 62, height = 24, state = 'disabled') ; chat_log.pack(side='left')#place(x=20, y=60)
chat_frame.place(x=20, y=60)
message_input = Text(window, width = 55, height = 4) ; message_input.place(x=20,y = 390)
send_button = Button(window, text = 'Send', command = lambda:send_func()); send_button.place(x=430, y=405)
​
​
sender=Thread(target=send_func, args=())
receiver=Thread(target=recv_func, args=())
sender.start()
receiver.start()
​
window.mainloop()
​

