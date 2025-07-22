from hashtable import HashTable, Pair
import pytest
from pytest_unordered import unordered

# Initialisation

def test_should_create_hash_table():
    assert HashTable(size=50) is not None

def test_should_create_pair():
    assert Pair(key="key", value="value") is not None

def test_should_fill_with_nones_on_init():
    assert HashTable(size=50)._slots == [None for _ in range(50)]

# Setting and getting pairs

@pytest.fixture(scope="module")
def hash_table():
    ht = HashTable(size=10)
    ht["hello"] = "world"
    ht[17] = 18
    ht[True] = False
    return ht

def test_should_insert_specific_pairs(hash_table):

    assert ("hello","world") in hash_table.pairs
    assert (17,18) in hash_table.pairs
    assert (True,False) in hash_table.pairs

def test_should_get_length_of_pairs(hash_table):
    assert len(hash_table) == 3

def test_should_get_specific_inserted_values_by_indexing(hash_table):
    assert hash_table["hello"] == "world"
    assert hash_table[17] == 18
    assert hash_table[True] == False

def test_should_get_pair_given_key(hash_table):
    assert hash_table.get("hello") == "world"
    assert hash_table.get("missing") is None


def test_should_raise_key_error_on_invalid_key():
    with pytest.raises(KeyError) as exception:
        ht = HashTable(size=10)["invalid_key"]

    assert exception.type == KeyError
    assert str(exception.value) == "'key not found'"

def test_should_get_all_keys(hash_table):
    assert hash_table.keys == {"hello",17,True}

def test_should_get_empty_keys_on_empty_hash_table():
    assert HashTable(10).keys == set()

def test_should_get_all_values(hash_table):
    assert unordered(hash_table.values) == ["world",18,False]

def test_should_get_empty_values_on_empty_hash_table():
    assert HashTable(10).values == []

def test_should_create_copies_of_data(hash_table):
    assert hash_table.pairs is not hash_table.pairs
    assert hash_table.keys is not hash_table.keys
    assert hash_table.values is not hash_table.values

def test_should_not_create_hashtable_with_non_positive_size():
    with pytest.raises(ValueError) as exception:
        HashTable(size=0)

    assert exception.type == ValueError

def test_should_report_size(hash_table):
    assert hash_table.size == 10

# Additional utility functionality

def test_should_print_pairs(hash_table):
    assert str(hash_table) in {"{'hello':'world', 17:18, True:False}",
                               "{17:18, 'hello':'world', True:False}",
                               "{True:False, 17:18, 'hello':'world'}",
                               "{'hello':'world', True:False, 17:18}",
                               "{17:18, 'hello':'world', True:False}",
                               "{True:False, 'hello':'world', 17:18}",
                               }

def test_should_make_from_dict(hash_table):
    assert HashTable.from_dict(dict(hash_table.pairs)) == hash_table

def test_should_make_from_dict_with_custom_size(hash_table):
    assert HashTable.from_dict(dict(hash_table.pairs), size = 10)

def test_should_raise_value_error_from_dict_with_custom_size_lower_than_size(hash_table):
    with pytest.raises(ValueError) as exception:
        HashTable.from_dict(dict(hash_table.pairs), size = 2)

    assert exception.type == ValueError

def test_should_repr_hash_table(hash_table):
    assert repr(hash_table) in {"HashTable({'hello':'world', 17:18, True:False})",
                                "HashTable({'hello':'world', True:False, 17:18})",
                                "HashTable({17:18, 'hello':'world', True:False})",
                                "HashTable({17:18, True:False, 'hello':'world'})",
                                "HashTable({True:False, 'hello':'world', 17:18})",
                                "HashTable({True:False, 17:18, 'hello':'world'})",
                                }

def test_should_copy_hash_table(hash_table):
    assert hash_table.copy() == hash_table
    assert hash_table.copy() is not hash_table


