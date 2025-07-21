from typing import NamedTuple


class Pair(NamedTuple):
    key: str
    value: str


class HashTable:

    @classmethod
    def from_dict(cls, pairs, size=10):
        if size < len(pairs):
            raise ValueError(f"size: {size} must be greater than or equal to the number of pairs: {len(pairs)}")
        ht = cls(size)
        for key, value in pairs.items():
            ht[key] = value
        return ht


    def __init__(self, size):
        if size < 1:
            raise ValueError("size must be greater than 0")
        self._slots = [None] * size

    @property
    def pairs(self):
        return {pair for pair in self._slots if pair}

    @property
    def keys(self):
        return {key for key, _ in self.pairs}

    @property
    def values(self):
        return [value for _, value in self.pairs]

    @property
    def size(self):
        return len(self._slots)

    def _get_index(self, key):
        return hash(key) % self.size

    def __len__(self):
        return len(self.pairs)

    def __setitem__(self, key, value):
        self._slots[self._get_index(key)] = Pair(key, value)

    def __getitem__(self, key):
        if pair := self._slots[self._get_index(key)] :
            return pair.value
        else:
            raise KeyError("key not found")

    def __str__(self):
        return "{" + str(", ".join([f"{key!r}:{value!r}"for key,value in self.pairs])) +"}"

    def __repr__(self):
        return f"{self.__class__.__name__}({str(self)})"

    def __eq__(self, other):
        return self.pairs == other.pairs

# TODO: Add other nonessential dict methods like copy,get
