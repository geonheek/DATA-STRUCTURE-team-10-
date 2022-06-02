import time
​
class Queue:
    def __init__(self):
        self.queue = []
​
    def isEmpty(self):
        if not self.queue:
            return True
        else:
            return False
​
    def enqueue(self, data):
        self.queue.append(data)
​
    def dequeue(self):
        if self.isEmpty():
            return "Queue is Empty"
        else:
            dequeued = self.queue[0]
            # 꺼낸 뒤 나머지 재정비
            self.queue = self.queue[1:]
            return dequeued
        
    def size(self):
        count = len(self.queue)
        return count
​
​
if __name__ == "__main__":
    q = Queue()
    count = 0
    start = time.time()
    while(1):
        msg = input('문자를 입력하시오')
        q.enqueue(msg)
        count += 1
        end = time.time()
        if(end - start > 10):
            for i in range(count):
                print(q.dequeue())
            break
