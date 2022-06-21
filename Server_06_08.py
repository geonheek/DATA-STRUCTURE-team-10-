# Server
from socket import *
from threading import *
from queue import *
import sys
import datetime
from hashtable import *
from linkedlist import *

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

def send_func(conn, count, lock):
    global c_list
    now_member_msg='현재 멤버 : '
    for mem in member_name_list:
        if mem!='-1':
            now_member_msg+='['+mem+'] '
    conn.send(now_member_msg.encode())
    msg=str(get_time()+member_name_list[count])+'님이 입장하였습니다.'
    for conn1 in socket_descriptor_list:
        if conn1 =='-1': # 연결 종료한 클라이언트 경우.
            continue
        elif conn1 != conn: #자신에게는 보내지 않음.
            conn1.send(msg.encode())
        else: 
            pass
     
    
    while True:
        try:
            recv = received_msg_info.get()
            if recv[0]=='!quit' or len(recv[0])==0:
                msg=str(get_time()+left_member_name)+'님이 연결을 종료하였습니다.'
            
            elif recv[0]=='!member':
                now_member_msg='현재 멤버 : '
                for mem in member_name_list:
                    if mem!='-1':
                        now_member_msg+='['+mem+'] '
                recv[1].send(now_member_msg.encode())
                recv[1].send(now_member_msg.encode())
                continue
            elif recv[0] == '!revise':
                continue
            else:
                msg = str(get_time() + member_name_list[recv[2]]) + ' : ' + str(recv[0])
                k = open("talk.txt","a") # user.txt 파일을 추가 모드(a)로 열기
                k.write(msg) # user.txt에 client_id 추가
                k.write(" ")
                k.write("\n")
                k.close() # user.txt에 client_info 추가

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
                for i in range(len(whisper_list)):
                    if whisper_list[i]==count:
                        whisper_list[i]=-1
                member_name_list[count]='-1'
                lock.release()
                break
            if data == '!revise':
                closed = Revise(conn, member_name_list[count])
                if closed == 0:
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
    client_id = None
    conn.send('send_your_ID_and_password'.encode())

    try:                                            # 회원가입: ID, password 입력
        client_id = conn.recv(1024).decode()
    except ConnectionAbortedError:
        closed = conn.close()
        return closed
    except ConnectionResetError:
        closed = conn.close()
        return closed
    if client_id == '!cancel':
        closed = 1
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
            if client_id == '!cancel':
                closed = 1
                return closed
            if not client_id in ID_list:
                break
    if not client_id == None:
        conn.send('send_your_info'.encode())
        try:
            client_info = conn.recv(1024).decode()
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
        ID_list.append(client_id) # 회원가입한 아이디들이 모두 저장되는 리스트 
        ID_pass2 = LinkedList() # 개개인의 정보들을 저장하는 링크드 리스트
        temp = client_info.split(' ')
        ID_pass2.append(temp[0])
        ID_pass2.append(temp[1])
        ID_pass2.append(temp[2])
        ID_pass2.append(temp[3])
        ID_pass2.append(temp[4])
        ID_pass2.append(temp[5])
        ID_pass2.append('white')
        ID_pass2.printlist()
        ID_pass.insert(client_id, ID_pass2) # [id, <linkedlist>]를 저장한 해시테이블
        ID_pass.print()

        f = open("user.txt","a") # user.txt 파일을 추가 모드(a)로 열기
        f.write(client_id) # user.txt에 client_id 추가
        f.write(" ")
        f.write(client_info) # user.txt에 client_info 추가
        f.write(" ")
        f.write('white')
        f.write("\n")
        f.close()

        return closed

def Revise(conn, client_id):
    closed = 1
    try:
        client_info = conn.recv(1024).decode()
    except ConnectionAbortedError:
        closed = 0
    except ConnectionResetError:
        closed = 0
    if client_info == '!cancel':
        print("a")
        closed = 1
    else:
        temp = client_info.split(' ')
        checking = ID_pass.read(client_id)
        if temp[0] != checking.selectNode(0).data:
            checking.selectNode(0).data = temp[0]
        if temp[1] != checking.selectNode(1).data:
            checking.selectNode(1).data = temp[1]
        if temp[2] != checking.selectNode(2).data:
            checking.selectNode(2).data = temp[2]
        if temp[3] != checking.selectNode(3).data:
            checking.selectNode(3).data = temp[3]
        if temp[4] != checking.selectNode(4).data:
            checking.selectNode(4).data = temp[4]
        if temp[5] != checking.selectNode(5).data:
            checking.selectNode(5).data = temp[5]
        ID_pass.insert(client_id, checking)
        closed = 1
    return closed


def connect(conn, addr, closed):
    global count
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
        client_name = ' '
        while True:
            try:                                                  # 1. 로그인 
                client_idpass=conn.recv(1024).decode()
                inputIDPASS = client_idpass.split(' ')        # inputIDPASS[0]: 아이디, inputIDPASS[1]: 패스워드
            except ConnectionAbortedError:
                closed = conn.close()
                break
            except ConnectionResetError:
                closed = conn.close()
                break
            if not inputIDPASS[0] in ID_list: # 아이디의 등록 여부 확인
                conn.send('ID_is_not_encounted'.encode())
            elif not inputIDPASS[0] in member_name_list: # 아이디의 접속 여부 확인 
                client_info_list = ID_pass.read(inputIDPASS[0]) # hashtable에서 linkedlist를 가져온 다음
                checkingpassword = client_info_list.selectNode(0)
                checkingblack = client_info_list.selectNode(6).data
                if checkingpassword.data == inputIDPASS[1]:  # 패스워드의 매칭 여부 확인
                    if checkingblack == 'black': 
                        conn.send('you_blocked'.encode())
                        continue
                    else:
                        conn.send('yes'.encode())
                    break
                else:
                    conn.send('wrongpassword'.encode())
            else:
                conn.send('overlapped'.encode())
        if closed == 1:
            try: 
                clientsaying = conn.recv(1024).decode()
            except ConnectionAbortedError:
                closed = conn.close()
            except ConnectionResetError:
                closed = conn.close()
            if closed == 1:
                client_info_list = ID_pass.read(inputIDPASS[0]) # 로그인한 아이디에 맞는 정보를 전송
                client_info0 = client_info_list.selectNode(0)
                client_info1 = client_info_list.selectNode(1)
                client_info2 = client_info_list.selectNode(2)
                client_info3 = client_info_list.selectNode(3)
                client_info4 = client_info_list.selectNode(4)
                client_info5 = client_info_list.selectNode(5)
                client_info = client_info0.data + ' ' + client_info1.data + ' ' + client_info2.data + ' ' + client_info3.data + ' ' + client_info4.data + ' ' + client_info5.data
                conn.send(client_info.encode())
        
        if closed == 1:
            count = count + 1
            member_name_list.append(inputIDPASS[0])
            socket_descriptor_list.append(conn)
            whisper_list.append(-1)
            print(str(get_time())+inputIDPASS[0]+'님이 연결되었습니다. 연결 ip : '+ str(addr[0]))

            
            
            if count>1:
                sender = Thread(target=send_func, args=(conn, count, lock))
                sender.start()
                pass
            else:
                sender=Thread(target=send_func, args=(conn, count, lock))
                sender.start()
            receiver=Thread(target=recv_func, args=(conn, count, lock))
            receiver.start()

print(get_time()+'서버를 시작합니다')
server_sock=socket(AF_INET, SOCK_STREAM)
server_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Time-wait 에러 방지.
server_sock.bind((HOST, PORT))
server_sock.listen()

count = 0
socket_descriptor_list=['-1',] # 클라이언트들의 소켓 디스크립터 저장.
member_name_list=['-1',] # 클라이언트들의 닉네임 저장, 인덱스 접근 편의를 위해 0번째 요소 '-1'로 초기화.
ID_list=['-1',] # 등록된 ID(현재 닉네임)를 저장하기 위한 임시 리스트
whisper_list=[-1,]

received_msg_info = Queue()
ID_pass = HashTable(100)
left_member_name=''
lock=Lock()

with open(r"user.txt", 'r') as userDB:    # user.txt 파일을 읽기 모드(r)로 열기
    lines = None
    lines = userDB.read() # read함수를 이용해 파일의 내용 전체를 문자열로 돌려줌
    splitline = lines.split() 

    print(lines)
    print(splitline)

    size = len(splitline)
    print(size)


    j=0 
    while j < size / 8:     # 문자열에 저장한 user 정보를 ID_list와 LinkedList에 저장
        user_info = LinkedList()
        client_id = ' '
        i=0
        while i < 8 :
            if(i % 8 == 0):
                ID_list.append(splitline[i + j * 8])
                client_id = splitline[i + j * 8]
            elif(i % 8 == 1):
                user_info.append(splitline[i + j * 8])
            elif(i % 8 == 2):
                user_info.append(splitline[i + j * 8])
            elif(i % 8 == 3):
                user_info.append(splitline[i + j * 8])
            elif(i % 8 == 4):
                user_info.append(splitline[i + j * 8])
            elif(i % 8 == 5):
                user_info.append(splitline[i + j * 8])
            elif(i % 8 == 6):
                user_info.append(splitline[i + j * 8])
            elif(i % 8 == 7):
                user_info.append(splitline[i + j * 8])
            i += 1

        user_info.printlist()
        ID_pass.insert(client_id, user_info)  # ID를 key로 user_info를 value로 Hashtable에 저장
        j += 1
        

print(ID_list)
ID_pass.print()


while True:
    closed = 1
    conn, addr = server_sock.accept()
        
    # conn과 addr에는 연결된 클라이언트의 정보가 저장된다.
    # conn : 연결된 소켓
    # addr[0] : 연결된 클라이언트의 ip 주소
    # addr[1] : 연결된 클라이언트의 port 번호

    connected = Thread(target=connect, args=(conn, addr, closed))
    connected.start()
    

server_sock.close()
