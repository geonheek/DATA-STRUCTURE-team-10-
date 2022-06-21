# Node 정의
class Node(object):
    def __init__(self, data,  next=None):
        self.data = data
        self.next = next


class LinkedList(object):
    def __init__(self):
        self.head = Node(None)
        self.size = 0

    def listSize(self): # O(1)
        return self.size

    def is_empty(self): # O(1)
        if self.size != 0:
            return False
        else:
            return True

    def selectNode(self, idx): # O(n) (아래와 같음)
        if idx >= self.size:
            print("Index Error")
            return None
        if idx == 0:
            return self.head
        else:
            target = self.head
            for cnt in range(idx):
                target = target.next
            return target

    # appendleft
    def appendleft(self, value): # O(1)
        if self.is_empty():
            self.head = Node(value)
        else:
            self.head = Node(value, self.head)
        self.size += 1

    # append
    def append(self, value): # O(n) (사실상 개인정보의 개수와 같으므로 상수시간이라 봐도 무방함)
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

    def printlist(self):
        target = self.head
        while target:
            if target.next != None:
                print(target.data, ' -  ', end='')
                target = target.next
            else:
                print(target.data)
                target = target.next

