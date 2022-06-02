class HashTable:
    def __init__(self):
        self.hash_table = list([0 for i in range(10)])
​
    def hash_function(self, key):
                return key % 10
​
    def insert(self, key, value):
          gen_key = hash(key)
          hash_value = self.hash_function(gen_key)
​
          if self.hash_table[hash_value] != 0:             # 해당 hash value index를 이미 사용하고 있는 경우(충돌 시)
            for i in range(len(self.hash_table[hash_value])):
              if self.hash_table[hash_value][i][0] == gen_key:     # 이미 같은 키 값이 존재하는 경우 -> value 교체
                  self.hash_table[hash_value][i][1] = value        # 이때 0은 key, 1은 value값이 존재하는 인덱스
                  return
            self.hash_table[hash_value].append([gen_key, value])      # 같은 키 값이 존재하지 않는 경우에는 [key, value]를 해당 인덱스에 삽입
          else:
            self.hash_table[hash_value] = [[gen_key, value]]      # 해당 hash_value를 사용하고 있지 않는 경우
​
    def read(self, key):
        gen_key = hash(key)
        hash_value = self.hash_function(gen_key)
        if self.hash_table[hash_value] != 0:
            for i in range(len(self.hash_table[hash_value])):
                if self.hash_table[hash_value][i][0] == gen_key:       # 해당 해쉬 값 index에 데이터가 존재할 때,
                  return self.hash_table[hash_value][i][1]             # 키와 동일할 경우 -> 해당 value return
            return None             # 동일한 키가 존재하지 않으면 None return
        else:
            return None             # 해당 해쉬 값 index에 데이터가 없을 때,
    
    def print(self):
        print(self.hash_table)

ht = HashTable() 
ht.insert(1, 'a') 
ht.print() 
ht.insert('Team', 'Team10') 
ht.print() 
ht.insert(2, 'b') 
ht.print() 
ht.insert(3, 'c') 
ht.print() 
print(ht.read(2))  
print(ht.read('Team')) 
