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
    for i in range(100):
        q.enqueue(i)
        if (q.size() >= 10):
          for i in range(10):
              print(q.dequeue())
          print("team10")    
    
​
​
    #큐 사이즈 측정
    #시간 측정 함수 구
