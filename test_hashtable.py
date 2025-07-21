from hashtable import HashTable


def test_should_create_hash_table():
    assert HashTable(size=50) is not None

def test_should_have_size():
    assert len(HashTable(size=50)) == 50

def test_should_have_none_values_on_initialisation():
    ht = HashTable(size=10)
    nones = [None for _ in range(10)]
    assert ht.values == nones

def test_should_insert_value():
    ht = HashTable(size=10)
    ht["John"] = "Smith"
    ht[52] = "Blah"
    ht["A"] = True
    assert "Smith" in ht.values
    assert "Blah" in ht.values
    assert True in ht.values
    assert len(ht.values) == len(ht)