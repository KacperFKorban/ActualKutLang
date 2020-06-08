class Memory:

    def __init__(self):
        self.dict = {}

    def has_key(self, name):
        return name in self.dict.keys()

    def get(self, name):
        return self.dict.get(name, None)

    def put(self, name, value):
        self.dict.update({name: value})

class MemoryStack:
                                      
    def __init__(self, memory=None):
        if memory is not None:
            self.memories = [memory]
        else:
            self.memories = [Memory()]

    def get(self, name):
        for m in self.memories:
            res = m.get(name)
            if res is not None:
                return res

    def insert(self, name, value):
        if len(self.memories) > 0:
            self.memories[0].put(name, value)

    def set(self, name, value):
        v = self.get(name)
        if v is None:
            self.insert(name, value)
        else:
            for m in self.memories:
                res = m.get(name)
                if name in m.dict.keys():
                    m.put(name, value)
                    break

    def push(self, memory):
        self.memories.insert(0, memory)

    def pop(self):
        return self.memories.pop(0)

    def push_back(self, memory):
        for m in memory.memories:
            self.memories.append(m)