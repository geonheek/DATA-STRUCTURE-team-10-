# Node 정의
class Node():
    def __init__(self, data, next=None):
        self.data = data
        self.next = next
​
​
class LinkedList():
    def __init__(self):
        self.head = Node(None)
        self.size = 0
​
    def listSize(self):
        return self.size
​
    def is_empty(self):
        return self.size ==0
​
    def sereach(self,a):
        target = self.head
        b = 0
        for i in range(0,self.size):
            if a in target.data:
                print(target.data)
                b+=1
                target = target.next
​
        if b ==0:
            print("찾은 데이터 없음\n")
            return 0
        else:
            print(b, " 개 발견\n")
            return b
​
​
​
    # append
    def append(self, value):
        if self.is_empty():
            self.head = Node(value)
            self.size += 1
        else:
            target = self.head
            while target.next != None:
                target = target.next
            newtail = Node(value)
            target.next = newtail
            self.size += 1
​
    # insert
    def insert(self, value, idx):
        if self.is_empty():
            self.head = Node(value)
            self.size += 1
        elif idx == 0:
            self.head = Node(value, self.head)
            self.size += 1
        else:
            target = self.selectNode(idx - 1)
            if target == None:
                return
            newNode = Node(value)
            tmp = target.next
            target.next = newNode
            newNode.next = tmp
            self.size += 1
​
    # delete
    def delete(self, idx):
        if self.is_empty():
            print('Underflow: Empty Linked List Error')
            return
        elif idx >= self.size:
            print('Overflow: Index Error')
            return
        elif idx == 0:
            target = self.head
            self.head = target.next
            del (target)
            self.size -= 1
        else:
            target = self.selectNode(idx - 1)
            deltarget = target.next
            target.next = target.next.next
            del (deltarget)
            self.size -= 1
​
    def printlist(self):
        target = self.head
        while target:
            if target.next != None:
                print(target.data, ' -  ', end='')
                target = target.next
            else:
                print(target.data)
                target = target.next
​
​
mylist = LinkedList()
mylist.append("홍길동 111 ddd")
mylist.append("홀길동 222 ddd")
mylist.append("가나다 329 kkk")
mylist.append("가나다 333 kkk")
mylist.append("가나다 444 kkk")
​
mylist.printlist()
a = input()
mylist.selectNode(a)
print(mylist.is_empty())
