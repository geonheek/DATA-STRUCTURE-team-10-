import hashlib

class HashTable:
    def __init__(self, table_size):
        self.size = table_size
        self.hash_table = [0 for a in range(self.size)]
        
    def getKey(self, data):        
        key_folding = 0
        for i in range(0, len(data)):
            key_folding += ord(data[i])  #ord(): 문자의 ASCII코드 리턴
        self.key = key_folding     
        return self.key
    
    def hashFunction(self, key):    # constant time: O(1)
        if isinstance(key, int):    # 만약 key 값이 정수형이라면
            return key % self.size   # 해시테이블 크기로 나눈 나머지를 반환

    def getAddress(self, key):      # constant time: O(1)
        myKey = self.getKey(key)
        hash_address = self.hashFunction(myKey)
        return hash_address
    
    def insert(self, key, value):  
        hash_address = self.getAddress(key)

        if self.hash_table[hash_address] != 0:             # 해시 충돌이 발생할 경우(해시 주소가 동일한 경우)
            for i in range(len(self.hash_table[hash_address])):
                if self.hash_table[hash_address][i][0] == key:     # 이미 같은 키 값이 존재하는 경우 데이터를 덮어씀
                     self.hash_table[hash_address][i][1] = value        # 이때 0은 key, 1은 value값이 존재하는 인덱스
                     return
                self.hash_table[hash_address].append([key, value])      # 같은 키 값이 존재하지 않는 경우에는 [key, value]를 해당 인덱스에 삽입
        else:
            self.hash_table[hash_address] = [[key, value]]      # 해당 hash_value를 사용하고 있지 않는 경우

    def read(self, key):
        hash_address = self.getAddress(key)

        if self.hash_table[hash_address] != 0:
            for i in range(len(self.hash_table[hash_address])):
                if self.hash_table[hash_address][i][0] == key:       # 해당 해쉬 값 index에 데이터가 존재할 때,
                    return self.hash_table[hash_address][i][1]            # 키와 동일할 경우 -> 해당 value return
                    
            return None             # 동일한 키가 존재하지 않으면 None return
        else:
            return None             # 해당 해쉬 값 index에 데이터가 없을 때, None return

    def delete(self, key):
        hash_address = self.getAddress(key)
        
        if self.hash_table[hash_address] != 0:
            for i in range(len(self.hash_table[hash_address])):
                if self.hash_table[hash_address][i][0] == key:       # 해당 해쉬 값 index에 데이터가 존재할 때,
                    if len(self.hash_table[hash_address]) == 1:      
                        self.hash_table[hash_address] = 0          
                    else:
                        del self.hash_table[hash_address][i]        
                    return
            return False                # 동일한 키가 존재하지 않으면 False return
        else:
            return False                # 해당 해쉬 값 index에 데이터가 없을 때, False return
    
    def print(self):
        print(self.hash_table)

