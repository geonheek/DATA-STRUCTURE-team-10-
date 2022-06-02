# Server
from socket import *
from threading import *
from queue import *
import sys
import datetime

#------------- 서버 세팅 -------------
HOST = '127.0.0.1' # 서버 ip 주소 .
PORT = 2021 # 사용할 포트 번호.
#------------------------------------

s=''
s+='\n  -------------< 사용 방법 >-------------'
s+='\n   연결 종료 : !q 입력 or ctrl + c    '
s+='\n   참여 중인 멤버 보기 : !member 입력      '        
s+='\n  --------------------------------------\n\n'

def get_time():
    now = datetime.datetime.now()
    time_str=now.strftime('[%H:%M] ')
    return time_str

def send_func(lock):
    global c_list
    while True:
        try:
            recv = received_msg_info.get()
            if recv[0]=='!quit' or len(recv[0])==0:
                print("left_member_name" + left_member_name)
                msg=str(get_time()+left_member_name)+'님이 연결을 종료하였습니다.'
            
            elif recv[0]=='!enter' or recv[0]=='!member':
                now_member_msg='현재 멤버 : '
                for mem in member_name_list:
                    if mem!='-1':
                        now_member_msg+='['+mem+'] '
                recv[1].send(now_member_msg.encode())
                if(recv[0]=='!enter'):
                     msg=str(get_time()+member_name_list[recv[2]])+'님이 입장하였습니다.'
                else:
                    recv[1].send(now_member_msg.encode())
                    continue         
            else:
                msg = str(get_time() + member_name_list[recv[2]]) + ' : ' + str(recv[0])

            for conn in socket_descriptor_list:
                if conn =='-1': # 연결 종료한 클라이언트 경우.
                    continue
                elif recv[1] != conn: #자신에게는 보내지 않음.
                    conn.send(msg.encode())
                else:
                    pass
            if recv[0] =='!quit':
                recv[1].close()
        except:
            pass

def recv_func(conn, count, lock):
    global left_member_name
    if socket_descriptor_list[count]=='-1':
        return -1
    while True:
        try:
            data = conn.recv(1024).decode()
            if data == '!quit' or len(data)==0:
                # len(data)==0 은 해당 클라이언트의 소켓 연결이 끊어진 경우에 대한 예외 처리임.
                lock.acquire()
                print(str(get_time()+ member_name_list[count]) + '님이 연결을 종료하였습니다.')
                left_member_name=member_name_list[count] # 종료한 클라이언트 닉네임 저장.

                received_msg_info.put([data, conn, count])
                socket_descriptor_list[count]= '-1'
                for i in range(len(whisper_list)):
                    if whisper_list[i]==count:
                        whisper_list[i]=-1
                member_name_list[count]='-1'
                lock.release()
                break
        except ConnectionResetError as e:
            data = '!quit'
            lock.acquire()
            print(str(get_time()+ member_name_list[count]) + '님이 연결을 종료하였습니다.')
            left_member_name=member_name_list[count] # 종료한 클라이언트 닉네임 저장.
           
            received_msg_info.put([data, conn, count])
            socket_descriptor_list[count]= '-1'
            for i in range(len(whisper_list)):
                if whisper_list[i]==count:
                    whisper_list[i]=-1
            member_name_list[count]='-1'
            lock.release()
            break
        else:
            received_msg_info.put([data, conn, count])
    conn.close()

def initialization(conn, closed):
    global ID_list
    global pass_list
    client_id = None
    client_pass = None
    conn.send('send_your_ID_and_password'.encode())

    try:                                            # 회원가입: ID, password 입력
        client_id = conn.recv(1024).decode()
    except ConnectionAbortedError:
        closed = conn.close()
        return closed
    except ConnectionResetError:
        closed = conn.close()
        return closed
    if client_id in ID_list:
        while True:
            conn.send('ID_is_duplicated'.encode())
            try:
                client_id = conn.recv(1024).decode()
            except ConnectionAbortedError:
                closed = conn.close()
                break
            except ConnectionResetError:
                closed = conn.close()
                break
            if not client_id in ID_list:
                break
    if not client_id == None:
        conn.send('send_your_password'.encode())
        try:
            client_pass = conn.recv(1024).decode()
        except ConnectionAbortedError:
            closed = conn.close()
            return closed
        except ConnectionResetError:
            closed = conn.close()
            return closed
        else:
            conn.send('encounted_your_encounter'.encode()) # 회원가입 후, 로그인
    if closed == 0:
        return closed
    if closed == 1:
        ID_list.append(client_id)
        password_list.append(client_pass)
        return closed

print(get_time()+'서버를 시작합니다')
server_sock=socket(AF_INET, SOCK_STREAM)
server_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Time-wait 에러 방지.
server_sock.bind((HOST, PORT))
server_sock.listen()

count = 0
socket_descriptor_list=['-1',] # 클라이언트들의 소켓 디스크립터 저장.
member_name_list=['-1',] # 클라이언트들의 닉네임 저장, 인덱스 접근 편의를 위해 0번째 요소 '-1'로 초기화.
ID_list=['-1',] # 등록된 ID(현재 닉네임)를 저장하기 위한 임시 리스트
password_list=['-1',] # 등록된 password를 저장하기 위한 임시 리스트
whisper_list=[-1,]

received_msg_info = Queue()
left_member_name=''
lock=Lock()

while True:
    closed = 1
    conn, addr = server_sock.accept()
        
    # conn과 addr에는 연결된 클라이언트의 정보가 저장된다.
    # conn : 연결된 소켓
    # addr[0] : 연결된 클라이언트의 ip 주소
    # addr[1] : 연결된 클라이언트의 port 번호

        
    while True:
        try:                                                # 회원가입/로그인 정보 입력 시도
            client_init = conn.recv(1024).decode()
        except ConnectionAbortedError:
            closed = conn.close()
            break
        except ConnectionResetError:
            closed = conn.close()
            break
        if client_init == '0':                              # 0. 회원가입 절차
            closed = initialization(conn, closed)
        elif client_init == '1': 
            conn.send('input_your_ID_and_password'.encode()) # 로그인으로 이동
            break
        else:
            conn.send('wrong input'.encode())
        if closed == None:
            break
        
    if closed == 1:
        while True:
            try:                                                  # 1. 로그인 
                client_name=conn.recv(1024).decode()
            except ConnectionAbortedError:
                closed = conn.close()
                break
            except ConnectionResetError:
                closed = conn.close()
                break
            if not client_name in ID_list:
                conn.send('ID_is_not_encounted'.encode())
            elif not client_name in member_name_list:
                conn.send('yes'.encode())
                break
            else:
                conn.send('overlapped'.encode())
        if closed == 1:
            member_name_list.append(client_name)
            socket_descriptor_list.append(conn)
            whisper_list.append(-1)
            print(str(get_time())+client_name+'님이 연결되었습니다. 연결 ip : '+ str(addr[0]))

            
            count = count +1
            if count>1:
                sender = Thread(target=send_func, args=(lock,))
                sender.start()
                pass
            else:
                sender=Thread(target=send_func, args=(lock,))
                sender.start()
            receiver=Thread(target=recv_func, args=(conn, count, lock))
            receiver.start()

server_sock.close()
