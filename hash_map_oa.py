# Name:
# OSU Email:
# Course: CS261 - Data Structures
# Assignment:
# Due Date:
# Description:


from a6_include import *


class HashEntry:

    def __init__(self, key: str, value: object):
        """
        Initializes an entry for use in a hash map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.key = key
        self.value = value
        self.is_tombstone = False

    def __str__(self):
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return f"K: {self.key} V: {self.value} TS: {self.is_tombstone}"


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses Quadratic Probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()

        for _ in range(capacity):
            self.buckets.append(None)

        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            out += str(i) + ': ' + str(self.buckets[i]) + '\n'
        return out

    def get_hashed_key(self, key: str) -> int:
        """
        Returns the given key hashed to the current capacity of the table.
        """
        return self.hash_function(key) % self.capacity

    def search_for_key(self, key: str) -> HashEntry:
        """
        Given a key, returns the matching HashEntry object if matched.
        If no match, returns the first replaceable index.
        """
        # Start at hashed index and quadratically probe until open space found.
        initial_index = self.get_hashed_key(key)
        modifier_index = 0
        probe_index = initial_index
        ts_index = None

        while self.buckets[probe_index] is not None:
            # Check if tombstone
            if self.buckets[probe_index].is_tombstone and ts_index is None:
                ts_index = probe_index
            elif self.buckets[probe_index].key == key:
                return self.buckets[probe_index]

            modifier_index += 1
            probe_index = (initial_index + modifier_index ** 2) % self.capacity

        # None reached, meaning the key was not found.
        return ts_index if ts_index is not None else probe_index

    def clear(self) -> None:
        """
        Clears the contents of the hash map while retaining capacity.
        """
        for index in range(self.buckets.length()):
            self.buckets[index] = None
        self.size = 0

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key, or None if not found.
        """
        # quadratic probing required
        search_result = self.search_for_key(key)
        return None if type(search_result) is int else search_result.value

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair if key already in hash map, else creates new KVP.
        """
        # remember, if the load factor is greater than or equal to 0.5,
        # resize the table before putting the new key/value pair
        #
        # quadratic probing required

        # Double capacity if current load factor >= 50%.
        if self.table_load() >= 0.5:
            self.resize_table(self.capacity * 2)

        # Search for the key
        result = self.search_for_key(key)
        if type(result) is int:                                  # Key was not found.
            self.buckets[result] = HashEntry(key, value)     # Add new entry to empty space.
            self.size += 1
        else:                                                   # Matching key found.
            result.value = value

    def remove(self, key: str) -> None:
        """
        Removes the entry with the given key from the hash table.
        If there is an entry, replaces with a tombstone.
        If not, does nothing.
        """
        # quadratic probing required
        search_result = self.search_for_key(key)
        if type(search_result) is not int:
            search_result.key = None
            search_result.value = None
            search_result.is_tombstone = True
            self.size -= 1

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, else False.
        """
        # quadratic probing required
        search_result = self.search_for_key(key)
        return type(search_result) is not int

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        return self.capacity - self.size

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """
        return self.size / self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes internal capacity of the hash table and rehashes all keys.
        Capacity cannot be < 1 or < number of elements currently in the map.
        """
        # remember to rehash non-deleted entries into new table

        # Validate
        if new_capacity < 1 or new_capacity < self.size:
            return

        # Store old entries
        old_array = DynamicArray()
        for index in range(self.buckets.length()):
            old_array.append(self.buckets[index])

        # Clear buckets and update capacity
        self.buckets = DynamicArray()
        self.capacity = new_capacity
        for _ in range(self.capacity):
            self.buckets.append(None)
        self.size = 0                               # Size will be rebuilt after "put" iterations

        # Rehash non-empty entries and add to new array
        for index in range(old_array.length()):
            element = old_array[index]
            if element is None:                     # Ignore empty values
                continue
            if element.is_tombstone:                # Ignore tombstones
                continue
            self.put(element.key, element.value)


    def get_keys(self) -> DynamicArray:
        """
        Returns a DynamicArray containing all the keys in the hash map in no particular order.
        """
        output = DynamicArray()
        for index in range(self.buckets.length()):
            element = self.buckets[index]
            if element is None:
                continue
            if element.is_tombstone:
                continue
            output.append(element.key)

        return output


if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    # this test assumes that put() has already been correctly implemented
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
