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
client_info = ' '
logined_id = ' '
closed = 0 # 연결이 닫혔는지 열렸는지 분간해주는 변수 (0: 닫힘, 1: 열림)

def now_time(): 
    now = datetime.datetime.now()
    time_str=now.strftime('[%H:%M] ')
    return time_str

def En_on_closing():
    global state
    global window2
    if state == 'Encount':
        send_data = '!cancel'
        try:
            client_sock.send(send_data.encode('utf-8'))
            login_button['state'] = 'active'
            En_button['state'] = 'active'
            state = 'initialization'
            window2.destroy()
        except ConnectionResetError:
            chat_log['state'] = 'normal'
            chat_log.insert("end",'\n' + '[공지] 서버와의 연결이 끊어졌습니다.')
            chat_log['state'] = 'disabled'
            window2.destroy()
            logout()


def Re_on_closing():
    global state
    global Re_window
    send_data = '!cancel'
    try:
        client_sock.send(send_data.encode('utf-8'))
        state = 'working'
        Re_window.destroy()
    except ConnectionResetError:
        chat_log['state'] = 'normal'
        chat_log.insert("end",'\n' + '[공지] 서버와의 연결이 끊어졌습니다.')
        chat_log['state'] = 'disabled'
        Re_window.destroy()
        logout()

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
    if closed != 0:
        while True:
            try:
                recv_data=(client_sock.recv(1024)).decode('utf-8')
                if len(recv_data)==0:
                    chat_log['state'] = 'normal'
                    chat_log.insert("end",'\n' + '[공지] 서버와의 연결이 끊어졌습니다.')
                    chat_log['state'] = 'disabled'
                    logout()
                    break
            except ConnectionAbortedError as e:
                logout()
                break
            except ConnectionResetError:
                chat_log['state'] = 'normal'
                chat_log.insert("end",'\n' + '[공지] 서버와의 연결이 끊어졌습니다.')
                chat_log['state'] = 'disabled'
                logout()
                break
            except OSError as e:
                logout()
                break
            except Exception as e:
                chat_log['state'] = 'normal'
                chat_log.insert("end",'\n' + '예외가 발생했습니다.' + e)
                chat_log.insert("end",'\n' + '[공지] 메시지를 수신하지 못하였습니다.')
                chat_log['state'] = 'disabled'
                logout()
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
    closed = 1
    try:
        client_sock.connect((Host,Port))
    except ConnectionRefusedError:
        chat_log['state'] = 'normal'
        chat_log.insert("end",'\n' + '서버에 연결할 수 없습니다.')
        chat_log.insert("end",'\n' + '1. 서버의 ip주소와 포트번호가 올바른지 확인하십시오.')
        chat_log.insert("end",'\n' + '2. 서버 실행 여부를 확인하십시오.')
        chat_log['state'] = 'disabled'
        closed = client_sock.close()
        return

    except:
        chat_log['state'] = 'normal'
        chat_log.insert("end",'\n' + '프로그램을 정상적으로 실행할 수 없습니다.')
        chat_log['state'] = 'disable'
        closed = client_sock.close()
        return
    else:
        chat_log['state'] = 'normal'
        chat_log.insert("end",'\n' + '[공지] 서버와 연결되었습니다.')
        chat_log.insert("end",'\n' + '원하시는 작업을 선택해주세요:  ')
        alive = 1
        state = 'initialization'
        login_button['state'] = 'active'
        logout_button['state'] = 'active'
        connect_button['state'] = 'disable'
        En_button['state'] = 'active'
        ip_entry['state'] = 'readonly'
        port_entry['state'] = 'readonly'
        chat_log['state'] = 'disabled'
        En_button['state'] = 'active'

def Encounter():   # 회원가입 시에 !cancel은 아이디로 사용할 수 없음
    global state
    global client_sock
    global window2
    global ID_entry2
    global pass_entry2
    global check_entry2
    global age_entry2
    global gender_entry2
    global job_entry2
    global birth_entry2
    global mail_entry2
    global En_button2
    if state == 'initialization':
        initial = '0' # 회원가입을 의미
        try:
            client_sock.send(initial.encode())
        except ConnectionResetError:
            chat_log['state'] = 'normal'
            chat_log.insert("end",'\n' + '[공지] 서버와의 연결이 끊어졌습니다.')
            chat_log['state'] = 'disabled'
            logout()
            return
        while True:
            response = client_sock.recv(1024).decode()
            if response == 'send_your_ID_and_password':
                chat_log['state'] = 'normal'
                chat_log.insert("end",'\n' + '가입하실 아이디와 패스워드를 입력하시고 회원가입 버튼을 눌러주세요')
                chat_log['state'] = 'disable'
                state = 'Encount'
                login_button['state'] = 'disable'
                ID_entry['state'] = 'disable'
                pass_entry['state'] = 'disable'
                En_button['state'] = 'disable'
                window2 = Tk()
                window2.title('회원가입')
                window2.geometry("300x300")
                window2.resizable(False, False)
                Label(window2, text = 'ID : ').place(x=30, y=10)
                Label(window2, text = 'Password : ').place(x=30, y=35)
                Label(window2, text = '나이: ').place(x=30, y=60)
                Label(window2, text = '성별: ').place(x=30, y=85)
                Label(window2, text = '직업: ').place(x=30, y=110)
                Label(window2, text = '생일: ').place(x=30, y=135)
                Label(window2, text = '이메일: ').place(x=30, y=160)
                ID_entry2 = Entry(window2, width=24); ID_entry2.place(x =100, y=10)
                pass_entry2 = Entry(window2, width=24); pass_entry2.place(x = 100, y=35)
                age_entry2 = Entry(window2, width=24); age_entry2.place(x = 100, y=60)
                gender_entry2 = Entry(window2, width=24); gender_entry2.place(x = 100, y=85)
                job_entry2 = Entry(window2, width=24); job_entry2.place(x = 100, y=110)
                birth_entry2 = Entry(window2, width=24); birth_entry2.place(x = 100, y=135)
                mail_entry2 = Entry(window2, width=24); mail_entry2.place(x = 100, y=160)
                check_entry2 = Entry(window2, width=24); check_entry2.place(x =100, y=185)
                check_entry2.insert(0, "checking entry")
                check_entry2['state'] = 'disable'
                En_button2 = Button(window2,text='신규 회원가입', command = Encounter); En_button2.place(x=100, y=210)
                window2.protocol("WM_DELETE_WINDOW", En_on_closing)
                return
            else:
                chat_log.insert("end",'\n' + response)
                return
    if state == 'Encount': # 회원가입 정보를 읽어들여서 전송하는 코드 
        client_id = (ID_entry2.get()).rstrip()
        client_pass = (pass_entry2.get()).rstrip()
        client_age = (age_entry2.get()).rstrip()
        client_gender = (gender_entry2.get()).rstrip()
        client_job = (job_entry2.get()).rstrip()
        client_birth = (birth_entry2.get()).rstrip()
        client_mail = (mail_entry2.get()).rstrip()

        if not client_id.strip():
            check_entry2['state'] = 'normal'
            check_entry2.delete(0,"end") 
            check_entry2.insert(0, '아이디를 입력해주세요.')
            check_entry2['state'] = 'disable'
            return
        if not client_pass.strip():
            check_entry2['state'] = 'normal'
            check_entry2.delete(0,"end") 
            check_entry2.insert(0, '패스워드를 입력해주세요.')
            check_entry2['state'] = 'disable'
            return
        if not client_age.strip():
            check_entry2['state'] = 'normal'
            check_entry2.delete(0,"end") 
            check_entry2.insert(0, '나이를 입력해주세요.')
            check_entry2['state'] = 'disable'
            return
        if not client_gender.strip():
            check_entry2['state'] = 'normal'
            check_entry2.delete(0,"end") 
            check_entry2.insert(0, '성별을 입력해주세요.')
            check_entry2['state'] = 'disable'
            return
        if not client_job.strip():
            check_entry2['state'] = 'normal'
            check_entry2.delete(0,"end") 
            check_entry2.insert(0, '직업을 입력해주세요.')
            check_entry2['state'] = 'disable'
            return
        if not client_birth.strip():
            check_entry2['state'] = 'normal'
            check_entry2.delete(0,"end") 
            check_entry2.insert(0, '생일을 입력해주세요.')
            check_entry2['state'] = 'disable'
            return
        if not client_mail.strip():
            check_entry2['state'] = 'normal'
            check_entry2.delete(0,"end") 
            check_entry2.insert(0, '이메일을 입력해주세요.')
            check_entry2['state'] = 'disable'
            return
        
        if client_id == '!cancel':
            check_entry2['state'] = 'normal'
            check_entry2.delete(0,"end") 
            check_entry2.insert(0, '해당 단어는 아이디로 사용할 수 없습니다.')
            check_entry2['state'] = 'disable'
            return
        if ' ' in client_id:
            check_entry2['state'] = 'normal'
            check_entry2.delete(0,"end") 
            check_entry2.insert(0, '공백은 입력이 불가능합니다.')
            check_entry2['state'] = 'disable'
            return
        if ' ' in client_pass:
            check_entry2['state'] = 'normal'
            check_entry2.delete(0,"end") 
            check_entry2.insert(0, '공백은 입력이 불가능합니다.')
            check_entry2['state'] = 'disable'
            return
        if ' ' in client_age:
            check_entry2['state'] = 'normal'
            check_entry2.delete(0,"end") 
            check_entry2.insert(0, '공백은 입력이 불가능합니다.')
            check_entry2['state'] = 'disable'
            return
        if ' ' in client_gender:
            check_entry2['state'] = 'normal'
            check_entry2.delete(0,"end") 
            check_entry2.insert(0, '공백은 입력이 불가능합니다.')
            check_entry2['state'] = 'disable'
            return
        if ' ' in client_job:
            check_entry2['state'] = 'normal'
            check_entry2.delete(0,"end") 
            check_entry2.insert(0, '공백은 입력이 불가능합니다.')
            check_entry2['state'] = 'disable'
            return
        if ' ' in client_birth:
            check_entry2['state'] = 'normal'
            check_entry2.delete(0,"end") 
            check_entry2.insert(0, '공백은 입력이 불가능합니다.')
            check_entry2['state'] = 'disable'
            return
        if ' ' in client_mail:
            check_entry2['state'] = 'normal'
            check_entry2.delete(0,"end") 
            check_entry2.insert(0, '공백은 입력이 불가능합니다.')
            check_entry2['state'] = 'disable'
            return

        try:
            client_sock.send(client_id.encode())    
        except ConnectionResetError:
            chat_log['state'] = 'normal'
            chat_log.insert("end",'\n' + '[공지] 서버와의 연결이 끊어졌습니다.')
            chat_log['state'] = 'disabled'
            logout()
            return
        response = client_sock.recv(1024).decode()
        if response == 'ID_is_duplicated':
            check_entry2['state'] = 'normal'
            check_entry2.delete(0,"end") 
            check_entry2.insert(0, 'ID가 중복됩니다')
            check_entry2['state'] = 'disable'
            return
        elif response == 'send_your_info':
            Encount_info = client_pass + ' ' + client_age + ' ' + client_gender + ' ' + client_job + ' ' + client_birth + ' ' + client_mail
            client_sock.send(Encount_info.encode())
        while True:
            response = client_sock.recv(1024).decode()
            if response == 'encounted_your_encounter':
                chat_log['state'] = 'normal'
                chat_log.insert("end",'\n' + client_id + '님, 회원 가입에 성공하셨습니다.  ')
                chat_log.insert("end",'\n' + '원하시는 작업을 선택해주세요:  ')
                chat_log['state'] = 'disable'
                login_button['state'] = 'active'
                En_button['state'] = 'active'
                state = 'initialization'
                window2.destroy()
                return
            else:
                chat_log.insert("end",'\n' + response)
                return
    if state == 'sleep':
        window2.destroy()

def Revise():
    global state
    global client_sock
    global Re_window
    global Re_pass_entry
    global Re_age_entry
    global Re_gender_entry
    global Re_job_entry
    global Re_birth_entry
    global Re_mail_entry
    global logined_id
    global client_info
    if state == 'working':
        state = 'revise'
        initial = '!revise'
        try:
            client_sock.send(initial.encode())
        except ConnectionResetError:
            chat_log['state'] = 'normal'
            chat_log.insert("end",'\n' + '[공지] 서버와의 연결이 끊어졌습니다.')
            chat_log['state'] = 'disabled'
            logout()
            return
        # 회원 정보 변경 창 세팅하는 코드,           
        Re_window = Tk()
        Re_window.title('회원정보 변경')
        Re_window.geometry("300x300")
        Re_window.resizable(False, False)
        Label(Re_window, text = 'ID : ').place(x=30, y=10)
        Label(Re_window, text = 'Password : ').place(x=30, y=35)
        Label(Re_window, text = '나이: ').place(x=30, y=60)
        Label(Re_window, text = '성별: ').place(x=30, y=85)
        Label(Re_window, text = '직업: ').place(x=30, y=110)
        Label(Re_window, text = '생일: ').place(x=30, y=135)
        Label(Re_window, text = '이메일: ').place(x=30, y=160)
        Re_ID_entry = Entry(Re_window, width=24); Re_ID_entry.place(x =100, y=10)
        Re_pass_entry = Entry(Re_window, width=24); Re_pass_entry.place(x = 100, y=35)
        Re_age_entry = Entry(Re_window, width=24); Re_age_entry.place(x = 100, y=60)
        Re_gender_entry = Entry(Re_window, width=24); Re_gender_entry.place(x = 100, y=85)
        Re_job_entry = Entry(Re_window, width=24); Re_job_entry.place(x = 100, y=110)
        Re_birth_entry = Entry(Re_window, width=24); Re_birth_entry.place(x = 100, y=135)
        Re_mail_entry = Entry(Re_window, width=24); Re_mail_entry.place(x = 100, y=160)
        Re_check_entry = Entry(Re_window, width=24); Re_check_entry.place(x =100, y=185)
        Re_En_button = Button(Re_window,text='회원정보 변경', command = Revise); Re_En_button.place(x=100, y=210)
        Re_check_entry.insert(0, "checking entry")
        Re_ID_entry.insert(0, logined_id)
        # 이곳에 서버로부터 받은 정보들을 입력하는 코드를 작성
        temp = client_info.split(' ')
        Re_pass_entry.insert(0, temp[0])
        Re_age_entry.insert(0, temp[1])
        Re_gender_entry.insert(0, temp[2])
        Re_job_entry.insert(0, temp[3])
        Re_birth_entry.insert(0, temp[4])
        Re_mail_entry.insert(0, temp[5])
        Re_ID_entry['state'] = 'disable'
        Re_check_entry['state'] = 'disable'
        
        Re_window.protocol("WM_DELETE_WINDOW", Re_on_closing)
        return
    
    if state == 'revise':
        client_pass = (Re_pass_entry.get()).rstrip()
        client_age = (Re_age_entry.get()).rstrip()
        client_gender = (Re_gender_entry.get()).rstrip()
        client_job = (Re_job_entry.get()).rstrip()
        client_birth = (Re_birth_entry.get()).rstrip()
        client_mail = (Re_mail_entry.get()).rstrip()

        if not client_pass.strip():
            Re_check_entry['state'] = 'normal'
            Re_check_entry.delete(0,"end") 
            Re_check_entry.insert(0, '패스워드를 입력해주세요.')
            Re_check_entry['state'] = 'disable'
            return
        if not client_age.strip():
            Re_check_entry['state'] = 'normal'
            Re_check_entry.delete(0,"end") 
            Re_check_entry.insert(0, '나이를 입력해주세요.')
            Re_check_entry['state'] = 'disable'
            return
        if not client_gender.strip():
            Re_check_entry['state'] = 'normal'
            Re_check_entry.delete(0,"end") 
            Re_check_entry.insert(0, '성별을 입력해주세요.')
            Re_check_entry['state'] = 'disable'
            return
        if not client_job.strip():
            Re_check_entry['state'] = 'normal'
            Re_check_entry.delete(0,"end") 
            Re_check_entry.insert(0, '직업을 입력해주세요.')
            Re_check_entry['state'] = 'disable'
            return
        if not client_birth.strip():
            Re_check_entry['state'] = 'normal'
            Re_check_entry.delete(0,"end") 
            Re_check_entry.insert(0, '생일을 입력해주세요.')
            Re_check_entry['state'] = 'disable'
            return
        if not client_mail.strip():
            Re_check_entry['state'] = 'normal'
            Re_check_entry.delete(0,"end") 
            Re_check_entry.insert(0, '이메일을 입력해주세요.')
            Re_check_entry['state'] = 'disable'
            return
        
        if ' ' in client_pass:
            Re_check_entry['state'] = 'normal'
            Re_check_entry.delete(0,"end") 
            Re_check_entry.insert(0, '공백은 입력이 불가능합니다.')
            Re_check_entry['state'] = 'disable'
            return
        if ' ' in client_age:
            Re_check_entry['state'] = 'normal'
            Re_check_entry.delete(0,"end") 
            Re_check_entry.insert(0, '공백은 입력이 불가능합니다.')
            Re_check_entry['state'] = 'disable'
            return
        if ' ' in client_gender:
            Re_check_entry['state'] = 'normal'
            Re_check_entry.delete(0,"end") 
            Re_check_entry.insert(0, '공백은 입력이 불가능합니다.')
            Re_check_entry['state'] = 'disable'
            return
        if ' ' in client_job:
            Re_check_entry['state'] = 'normal'
            Re_check_entry.delete(0,"end") 
            Re_check_entry.insert(0, '공백은 입력이 불가능합니다.')
            Re_check_entry['state'] = 'disable'
            return
        if ' ' in client_birth:
            Re_check_entry['state'] = 'normal'
            Re_check_entry.delete(0,"end") 
            Re_check_entry.insert(0, '공백은 입력이 불가능합니다.')
            Re_check_entry['state'] = 'disable'
            return
        if ' ' in client_mail:
            Re_check_entry['state'] = 'normal'
            Re_check_entry.delete(0,"end") 
            Re_check_entry.insert(0, '공백은 입력이 불가능합니다.')
            Re_check_entry['state'] = 'disable'
            return
        client_info = client_pass + ' ' + client_age + ' ' + client_gender + ' ' + client_job + ' ' + client_birth + ' ' + client_mail
        try:
            client_sock.send(client_info.encode())
        except ConnectionResetError:
            chat_log['state'] = 'normal'
            chat_log.insert("end",'\n' + '[공지] 서버와의 연결이 끊어졌습니다.')
            chat_log['state'] = 'disabled'
            logout()
            return
        print(client_info)
        Re_window.destroy()
        state = 'working'
        return
        
            
def login():
    global state
    global client_sock
    global logined_id
    global client_info
    En_button['state'] = 'disable'
    if state == 'initialization':
        ID_entry['state'] = 'normal'
        pass_entry['state'] = 'normal'
        initial = '1' # 로그인을 의미
        try:
            client_sock.send(initial.encode())
        except ConnectionResetError:
            chat_log['state'] = 'normal'
            chat_log.insert("end",'\n' + '[공지] 서버와의 연결이 끊어졌습니다.')
            chat_log['state'] = 'disabled'
            logout()
            return
        while True:
            response = client_sock.recv(1024).decode()
            if response == 'input_your_ID_and_password':
                chat_log['state'] = 'normal'
                chat_log.insert("end",'\n' + '로그인을 시작합니다.')
                chat_log.insert("end",'\n' + '로그인할 아이디와 패스워드를 입력하세요')
                chat_log['state'] = 'disable'
                state = 'login'
                return
            else:
                chat_log.insert("end",'\n' + response)
                return
    if state == 'login':                                    # 2. 회원가입이 끝났거나, 혹은 1을 입력했을 경우,
        client_id = (ID_entry.get()).rstrip()
        client_pass = (pass_entry.get()).rstrip()
        if not client_id.strip():
            chat_log['state'] = 'normal'
            chat_log.insert("end",'\n' + '공백은 입력이 불가능합니다.')
            chat_log['state'] = 'disable'
            return
        if not client_pass.strip():
            chat_log['state'] = 'normal'
            chat_log.insert("end",'\n' + '공백은 입력이 불가능합니다.')
            chat_log['state'] = 'disable'
            return
        if ' ' in client_id:
            chat_log['state'] = 'normal'
            chat_log.insert("end",'\n' + '공백은 입력이 불가능합니다.')
            chat_log['state'] = 'disable'
            return
        if ' ' in client_pass:
            chat_log['state'] = 'normal'
            chat_log.insert("end",'\n' + '공백은 입력이 불가능합니다.')
            chat_log['state'] = 'disable'
            return
        client_idpass = client_id + ' ' + client_pass
        try:
            client_sock.send(client_idpass.encode())
        except ConnectionResetError:
            chat_log['state'] = 'normal'
            chat_log.insert("end",'\n' + '[공지] 서버와의 연결이 끊어졌습니다.')
            chat_log['state'] = 'disabled'
            logout()
            return
        is_possible_name=client_sock.recv(1024).decode()
        if is_possible_name=='yes':
            logined_id = client_id
            chat_log['state'] = 'normal'
            chat_log.insert("end",'\n' + client_id + '님, 채팅방에 입장하였습니다.')
            pass_entry.delete(0,"end")
            chat_log['state'] = 'disable'
            client_sock.send('send_my_information'.encode())
            state = 'working'
            ID_entry['state'] = 'disable'
            pass_entry['state'] = 'disable'
            Re_button['state'] = 'active'
        elif is_possible_name=='ID_is_not_encounted':
            chat_log['state'] = 'normal'
            chat_log.insert("end",'\n' + '[공지] ID가 등록되어있지 않습니다.')
            chat_log['state'] = 'disable'
            return
        elif is_possible_name=='overlapped':
            chat_log['state'] = 'normal'
            chat_log.insert("end",'\n' + '[공지] 이미 사용중인 아이디입니다.')
            chat_log['state'] = 'disable'
            return
        elif is_possible_name=='you_blocked':
            chat_log['state'] = 'normal'
            chat_log.insert("end",'\n' + '[공지] 해당 아이디는 차단되었습니다. ')
            chat_log['state'] = 'disable'
            return
        elif is_possible_name=='wrongpassword':
            chat_log['state'] = 'normal'
            chat_log.insert("end",'\n' + '[공지] 패스워드가 다릅니다.')
            chat_log['state'] = 'disable'
            return
        elif len(client_sock.recv(1024).decode())==0:
            chat_log['state'] = 'normal'
            chat_log.insert("end",'\n' + '[공지] 서버와의 연결이 끊어졌습니다.')
            chat_log['state'] = 'disable'
            state = 'sleep'
            closed = client_sock.close()
            return
        client_info = client_sock.recv(1024).decode()
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
    global logined_id
    global client_info
    login_button['state'] = 'disable'
    logout_button['state'] = 'disable'
    connect_button['state'] = 'active'
    send_button['state'] = 'disable'
    En_button['state'] = 'disable'
    Re_button['state'] = 'disable'
    ip_entry['state'] = 'normal'
    port_entry['state'] = 'normal'
    ID_entry['state'] = 'normal'
    ID_entry.delete(0,"end")
    pass_entry.delete(0,"end")
    ID_entry['state'] = 'disable'
    pass_entry['state'] = 'disable'
    client_info = ' '
    logined_id = ' '
    if alive == 1:
        chat_log['state'] = 'normal'
        chat_log.insert("end",'\n' + '연결을 종료합니다.  ')
        chat_log['state'] = 'disable'
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
Label(window, text = 'ID : ').place(x=490, y=10)
Label(window, text = 'Password : ').place(x=490, y=30)
ip_entry = Entry(window, width=14); ip_entry.place(x=80, y=21)
ip_entry.insert(0,Host)
port_entry = Entry(window, width=5); port_entry.place(x = 220, y=21)
port_entry.insert(0, Port)
ID_entry = Entry(window, width=16, state = 'readonly'); ID_entry.place(x = 560, y=10)
pass_entry = Entry(window, width=16, state = 'readonly'); pass_entry.place(x = 560, y=30)
connect_button = Button(window,text='connect', command=connect); connect_button.place(x=270, y=18)
En_button = Button(window,text='회원가입',state = 'disabled', command = Encounter); En_button.place(x=330, y=18)
Re_button = Button(window,text='회원정보 변경',state = 'disabled', command = Revise); Re_button.place(x=395, y=18)
                      
login_button = Button(window,text='Login',state = 'disabled', command = login); login_button.place(x=690, y=18)
logout_button = Button(window,text='Logout',state = 'disabled', command = logout); logout_button.place(x=740, y=18)

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



