from typing import NamedTuple

DELETED = object()

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
        return {pair for pair in self._slots if pair and pair is not DELETED}

    @property
    def keys(self):
        return {key for key, _ in self.pairs}

    @property
    def values(self):
        return [value for _, value in self.pairs]

    @property
    def size(self):
        return len(self._slots)

    def get(self, key):
        if key not in self.keys:
            return None

        val = self._slots[self._get_index(key)].value

        return val

    def copy(self):
        return HashTable.from_dict(dict(self.pairs), size=self.size)

    def _get_index(self, key):
        index = hash(key) % len(self._slots)

        return index

    def _probe(self, key):
        index = self._get_index(key)
        for _ in range(self.size):
            yield self._slots[index], index
            index = (index + 1) % self.size

    def __len__(self):
        return len(self.pairs)

    def __setitem__(self, key, value):
        for pair, index in self._probe(key):
            if pair is DELETED:
                continue
            if pair is None or pair.key == key:
                self._slots[index] = Pair(key, value)
                break
        else:
            raise MemoryError("Hash table is full")

    def __getitem__(self, key):
        for pair, _ in self._probe(key):
            if pair is None:
                raise KeyError(key)
            if pair is DELETED:
                continue
            if pair.key == key:
                return pair.value
        raise KeyError(key)

    def __delitem__(self, key):
        for pair, index in self._probe(key):
            if pair is None:
                raise KeyError(key)
            if pair is DELETED:
                continue
            if pair.key == key:
                self._slots[index] = DELETED
                break
        else:
            raise KeyError(key)


    def __str__(self):
        return "{" + str(", ".join([f"{key!r}:{value!r}"for key,value in self.pairs])) +"}"

    def __repr__(self):
        return f"{self.__class__.__name__}({str(self)})"

    def __iter__(self):
        for pair in self.pairs:
            yield pair.key, pair.value

    def __eq__(self, other):
        return self.pairs == other.pairs and self.size == other.size


# TODO: Implement various hash functions, add optionality
