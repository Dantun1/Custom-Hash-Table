from typing import NamedTuple, Optional, Literal, TypeVar, Hashable, Generic

KT = TypeVar("KT", bound=Hashable)
VT = TypeVar("VT")

DELETED = object()

class Pair(NamedTuple):
    key: KT
    value: VT


class HashTable(Generic[KT, VT]):
    @classmethod
    def from_dict(cls, pairs, size=10):
        if size < len(pairs):
            raise ValueError(f"size: {size} must be greater than or equal to the number of pairs: {len(pairs)}")
        ht = cls(size)
        for key, value in pairs.items():
            ht[key] = value
        return ht


    def __init__(self, size, lf_threshold=0.6):
        if size < 1:
            raise ValueError("size must be greater than 0")
        if not lf_threshold > 0 and lf_threshold <= 1:
            raise ValueError("load factor threshold must be greater than 0 and less than or equal to 1")

        self._slots: list[Optional[Pair | Literal[DELETED]]] = [None] * size
        self._occupied_count = 0
        self._active_count = 0
        self._lf_threshold = lf_threshold

    @property
    def pairs(self) -> set[Pair]:
        return {pair for pair in self._slots if pair and pair is not DELETED}

    @property
    def keys(self) -> set[KT]:
        return {key for key, _ in self.pairs}

    @property
    def values(self) -> list[VT]:
        return [value for _, value in self.pairs]

    @property
    def size(self) -> int:
        return len(self._slots)

    @property
    def load_factor(self) -> float:
        return self._occupied_count / self.size

    def get(self, key) -> Optional[VT]:
        try:
            return self[key]
        except KeyError:
            return None


    def copy(self) -> "HashTable":
        return HashTable.from_dict(dict(self.pairs), size=self.size)

    def _resize_and_rehash(self):
        copy = HashTable.from_dict(dict(self.pairs), size=self.size * 2)
        self._slots = copy._slots

    def _get_index(self, key) -> int:
        index = hash(key) % len(self._slots)
        return index

    def _probe(self, key):
        index = self._get_index(key)
        for _ in range(self.size):
            yield self._slots[index], index
            index = (index + 1) % self.size

    def __len__(self):
        return self._active_count

    def __setitem__(self, key, value):
        if self.load_factor >= self._lf_threshold:
            self._resize_and_rehash()

        # Record the first index after the proper hash index that is available for insertion (including DELETED slots).
        first_available = -1
        for pair, index in self._probe(key):
            if pair is DELETED:
                if first_available == -1:
                    first_available = index
                continue

            if pair is None:
                # Insert into the first DELETED slot, or new slot at the end as the key doesn't exist in the chain.
                if first_available == -1:
                    # Occupied count only increments if a new slot is used (not DELETED).
                    self._occupied_count += 1
                    first_available = index
                self._slots[first_available] = Pair(key, value)
                self._active_count += 1
                break
            if pair.key == key:
                # Simply update the value if the key already exists
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
                self._active_count -= 1
                break
        else:
            raise KeyError(key)


    def __str__(self):
        return "{" + str(", ".join([f"{key!r}:{value!r}"for key,value in self.pairs])) +"}"

    def __repr__(self):
        return f"{self.__class__.__name__}({str(self)})"

    def __iter__(self):
        for pair in self._slots:
            if pair is not None and pair is not DELETED:
                yield pair

    def __eq__(self, other):
        if self._active_count != other._active_count:
            return False

        return self.pairs == other.pairs
