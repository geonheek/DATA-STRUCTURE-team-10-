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

state = 'sleep'
closed = 0 # 연결이 닫혔는지 열렸는지 분간해주는 변수 (0: 닫힘, 1: 열림)

def now_time(): 
    now = datetime.datetime.now()
    time_str=now.strftime('[%H:%M] ')
    return time_str

def send_func(): # 로그인 기능을 send_func 함수에서 구현
    global state
    global client_sock
    if state == 'working':
        send_data=(message_input.get(1.0, "end")).rstrip()
        client_sock.send(send_data.encode('utf-8'))
        chat_log['state'] = 'normal'
        chat_log.insert("end",'\n' + now_time() + send_data)
        chat_log['state'] = 'disabled'
        message_input.delete(1.0, "end")

def recv_func():
    global client_sock
    global state
    global closed
    if state == 'working':
        if closed != 0:
            while True:
                try:
                    recv_data=(client_sock.recv(1024)).decode('utf-8')
                    if len(recv_data)==0:
                        chat_log['state'] = 'normal'
                        chat_log.insert("end",'\n' + '[공지] 서버와의 연결이 끊어졌습니다.')
                        chat_log['state'] = 'disabled'
                        state = 'sleep'
                        alive = 0
                        closed = client_sock.close()
                        os._exit(1)
                except Exception as e:
                    chat_log['state'] = 'normal'
                    chat_log.insert("end",'\n' + '예외가 발생했습니다.' + e)
                    chat_log.insert("end",'\n' + '[공지] 메시지를 수신하지 못하였습니다.')
                    chat_log['state'] = 'disabled'
                    state = 'sleep'
                    alive = 0
                    closed = client_sock.close()
                    os._exit(1)
                else:
                    chat_log['state'] = 'normal'
                    chat_log.insert("end",'\n' + recv_data)
                    chat_log['state'] = 'disabled'
                    pass
            
    
def connect():
    global client_sock
    global alive
    global state
    global closed
    Host = ip_entry.get(); Port = int(port_entry.get())
    client_sock=socket(AF_INET, SOCK_STREAM)
    chat_log['state'] = 'normal'
    closed = 1
    try:
        client_sock.connect((Host,Port))
    except ConnectionRefusedError:
        chat_log.insert("end",'\n' + '서버에 연결할 수 없습니다.')
        chat_log.insert("end",'\n' + '1. 서버의 ip주소와 포트번호가 올바른지 확인하십시오.')
        chat_log.insert("end",'\n' + '2. 서버 실행 여부를 확인하십시오.')
        chat_log['state'] = 'disabled'
        closed = client_sock.close()
        return

    except:
        chat_log.insert("end",'\n' + '프로그램을 정상적으로 실행할 수 없습니다.')
        chat_log['state'] = 'disable'
        closed = client_sock.close()
        return
    else:
        chat_log.insert("end",'\n' + '[공지] 서버와 연결되었습니다.')
        alive = 1
        chat_log.insert("end",'\n' + '원하시는 작업을 선택해주세요:  ')
        state = 'initialization'
        login_button['state'] = 'active'
        logout_button['state'] = 'active'
        connect_button['state'] = 'disable'
        En_button['state'] = 'active'
        ip_entry['state'] = 'readonly'
        port_entry['state'] = 'readonly'
        chat_log['state'] = 'disabled'
        En_button['state'] = 'active'

def Encounter():
    global state
    global client_sock
    if state == 'initialization':
        ID_entry['state'] = 'normal'
        pass_entry['state'] = 'normal'
        initial = '0' # 회원가입을 의미
        client_sock.send(initial.encode())
        chat_log['state'] = 'normal'
        while True:
            response = client_sock.recv(1024).decode()
            if response == 'send_your_ID_and_password':
                chat_log.insert("end",'\n' + '가입하실 아이디와 패스워드를 입력하시고 회원가입 버튼을 눌러주세요')
                login_button['state'] = 'disable'
                state = 'Encount'
                return
            else:
                chat_log.insert("end",'\n' + response)
                return
    if state == 'Encount':
        client_id = (ID_entry.get()).rstrip()
        client_pass = (pass_entry.get()).rstrip()
        ID_entry.delete(0,"end")
        pass_entry.delete(0,"end")
        if not client_id.strip():
            chat_log.insert("end",'\n' + '공백은 입력이 불가능합니다.')
            return
        if not client_pass.strip():
            chat_log.insert("end",'\n' + '공백은 입력이 불가능합니다.')
            return
        if ' ' in client_id:
            chat_log.insert("end",'\n' + '공백은 입력이 불가능합니다.')
            return
        if ' ' in client_pass:
            chat_log.insert("end",'\n' + '공백은 입력이 불가능합니다.')
            return
        client_sock.send(client_id.encode())
        response = client_sock.recv(1024).decode()
        if response == 'ID_is_duplicated':
            chat_log.insert("end",'\n' + 'ID가 중복됩니다')
            return
        elif response == 'send_your_password':
            client_sock.send(client_pass.encode())
        while True:
            response = client_sock.recv(1024).decode()
            if response == 'encounted_your_encounter':
                chat_log['state'] = 'normal'
                chat_log.insert("end",'\n' + client_id + '님, 회원 가입에 성공하셨습니다.  ')
                chat_log.insert("end",'\n' + '원하시는 작업을 선택해주세요:  ')
                login_button['state'] = 'active'
                state = 'initialization'
                ID_entry['state'] = 'disable'
                pass_entry['state'] = 'disable'
                return
            else:
                chat_log.insert("end",'\n' + response)
                return
            
def login():
    global state
    global client_sock
    En_button['state'] = 'disable'
    if state == 'initialization':
        ID_entry['state'] = 'normal'
        pass_entry['state'] = 'normal'
        initial = '1' # 로그인을 의미 
        client_sock.send(initial.encode())
        chat_log['state'] = 'normal'
        while True:
            response = client_sock.recv(1024).decode()
            if response == 'input_your_ID_and_password':
                chat_log.insert("end",'\n' + '로그인을 시작합니다.')
                chat_log.insert("end",'\n' + '로그인할 아이디와 패스워드를 입력하세요')
                state = 'login'
                return
            else:
                chat_log.insert("end",'\n' + response)
                return
    if state == 'login':                                    # 2. 회원가입이 끝났거나, 혹은 1을 입력했을 경우,
        client_id = (ID_entry.get()).rstrip()
        client_pass = (pass_entry.get()).rstrip()
        ID_entry.delete(0,"end")
        pass_entry.delete(0,"end")
        if not client_id.strip():
            chat_log.insert("end",'\n' + '공백은 입력이 불가능합니다.')
            return
        if not client_pass.strip():
            chat_log.insert("end",'\n' + '공백은 입력이 불가능합니다.')
            return
        if ' ' in client_id:
            chat_log.insert("end",'\n' + '공백은 입력이 불가능합니다.')
            return
        if ' ' in client_pass:
            chat_log.insert("end",'\n' + '공백은 입력이 불가능합니다.')
            return
        client_sock.send(client_id.encode())
        is_possible_name=client_sock.recv(1024).decode()
        if is_possible_name=='yes':
            chat_log.insert("end",'\n' + client_id + '님, 채팅방에 입장하였습니다.')
            client_sock.send('!enter'.encode())
            state = 'working'
            ID_entry['state'] = 'disable'
            pass_entry['state'] = 'disable'
        elif is_possible_name=='ID_is_not_encounted':
            chat_log.insert("end",'\n' + 'ID가 등록되어있지 않습니다.')
            return
        elif is_possible_name=='overlapped':
            chat_log.insert("end",'\n' + '[공지] 이미 사용중인 닉네임입니다.')
            return
        elif len(client_sock.recv(1024).decode())==0:
            chat_log.insert("end",'\n' + '[공지] 서버와의 연결이 끊어졌습니다.')
            state = 'sleep'
            closed = client_sock.close()
            return
        send_button['state'] = 'active'
        login_button['state'] = 'disable'
        sender=Thread(target=send_func, args=())
        receiver=Thread(target=recv_func, args=())
        sender.start()
        receiver.start()
        return

    
def logout():
    global alive
    global state
    login_button['state'] = 'disable'
    logout_button['state'] = 'disable'
    connect_button['state'] = 'active'
    send_button['state'] = 'disable'
    ip_entry['state'] = 'normal'
    port_entry['state'] = 'normal'
    ID_entry.delete(0,"end")
    pass_entry.delete(0,"end")
    ID_entry['state'] = 'disable'
    pass_entry['state'] = 'disable'
    if alive == 1:
        send_data = '!quit'
        client_sock.send(send_data.encode('utf-8'))
        closed = client_sock.close()
        alive = 0
        state = 'sleep'
    return


alive = 0   # connect 상태를 가리킴: (0: 미연결 / 1: 서버와 연결 성사)
client_sock=socket(AF_INET, SOCK_STREAM)

# tkinter GUI의 기본 토대
window = Tk()
window.title('채팅 프로그램: client')
window.geometry("800x500")
window.resizable(False, False)

# ID와 password를 입력받는 창, login/logout 버튼
Label(window, text = 'Server IP : ').place(x=20, y=20)
Label(window, text = 'Port : ').place(x=185, y=20)
Label(window, text = 'ID : ').place(x=440, y=10)
Label(window, text = 'Password : ').place(x=440, y=30)
ip_entry = Entry(window, width=14); ip_entry.place(x=80, y=21)
ip_entry.insert(0,Host)
port_entry = Entry(window, width=5); port_entry.place(x = 220, y=21)
port_entry.insert(0, Port)
ID_entry = Entry(window, width=16, state = 'readonly'); ID_entry.place(x = 510, y=10)
pass_entry = Entry(window, width=16, state = 'readonly'); pass_entry.place(x = 510, y=30)
connect_button = Button(window,text='connect', command=connect); connect_button.place(x=270, y=18)
En_button = Button(window,text='신규 회원가입',state = 'disabled', command = Encounter); En_button.place(x=340, y=18)
                      
login_button = Button(window,text='Login',state = 'disabled', command = login); login_button.place(x=680, y=18)
logout_button = Button(window,text='Logout',state = 'disabled', command = logout); logout_button.place(x=730, y=18)

# 채팅 로그와 전송 입력창을 가리킴
chat_frame = Frame(window)
scrollbar = Scrollbar(chat_frame) ; scrollbar.pack(side='right',fill='y')
chat_log = Text(chat_frame, width = 107, height = 24, state = 'disabled') ; chat_log.pack(side='left')
scrollbar['command'] = chat_log.yview
chat_frame.place(x=20, y=60)
message_input = Text(window, width = 97, height = 4) ; message_input.place(x=20,y = 390)
send_button = Button(window, text = 'Send', state = 'disable', command = lambda:send_func()); send_button.place(x=720, y=405)

sender=Thread(target=send_func, args=())
receiver=Thread(target=recv_func, args=())
sender.start()
receiver.start()

window.mainloop()



