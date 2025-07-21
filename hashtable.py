class HashTable:
    def __init__(self, size):
        self.size = size
        self.values = [None] * size

    def __len__(self):
        return self.size

    def __setitem__(self, key, value):
        index = hash(key) % len(self)
        self.values[index] = value


