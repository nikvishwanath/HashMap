# HashMap - Separate Chaining Implementation 

from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)

class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        """
        return self._capacity

    
    def put(self, key: str, value: object) -> None:
        """
        Takes as a parameter a key and value pair, and adds them to the HashMap.  
        """
        
        # Insertion index.  
        index = self._hash_function(key) % self._buckets.length()
        
        # If the given key already exists in the HashMap, update its value.  
        if self.contains_key(key):
            nodes = self._buckets.get_at_index(index)
            for node in nodes:
                if node.key == key:
                    node.value = value
        # Otherwise insert it.  
        else:  
            self._buckets.get_at_index(index).insert(key, value)
        
        self._size += 1

    def empty_buckets(self) -> int:
        """
        Takes no parameters, and returns the number of empty buckets in the HashMap.  
        """
        empty_buckets = 0 
        # Count the number of empty buckets in the array.  
        for index in range(self._buckets.length()):
            if self._buckets.get_at_index(index).length() == 0:
                empty_buckets += 1
        return empty_buckets

    def table_load(self) -> float:
        """
        Takes no parameters, and returns the load factor of the HashMap.
        """
        
        return self.get_size() / self._buckets.length()

    def clear(self) -> None:
        """
        Takes no parameters, and clears the contents of the HashMap.
        """
        for i in range(self._buckets.length()):
            self._buckets.set_at_index(i, LinkedList())
        
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Takes as a parameter a new capacity, and resizes the HashMap to that capacity.  
        """
        
        array_capacity = None

        # Determine new capacity.   
        if new_capacity < 1:
            return
        if self._is_prime(new_capacity):
            array_capacity = new_capacity
        else:
            next_prime = self._next_prime(new_capacity)
            array_capacity = next_prime
        
        # Dynamic Array with new capacity.  
        da = DynamicArray()
        for i in range(array_capacity):
            da.append(LinkedList())
        
        # Rehash. 
        for index in range(self._buckets.length()):
            nodes = self._buckets.get_at_index(index)
            for node in nodes:
                index = self._hash_function(node.key) % array_capacity
                da.get_at_index(index).insert(node.key, node.value)
        
        # Assign new array and update capacity.  
        self._buckets = da
        self._capacity = array_capacity

    def get(self, key: str) -> object:
        """
        Takes as a paramter a key, and returns the associated value.  
        """
        index = self._hash_function(key) % self._buckets.length()

        # If the key is in the HashMap, iterate through the linked list until it is found 
        # and return the associated value.  
        if self._buckets.get_at_index(index).contains(key):
            node = self._buckets.get_at_index(index)
            for i in node:
                if i.key == key:
                    return i.value
        # Returns None if the key is not in the HashMap.          
        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        Takes as a parameter a key, and returns True if the key is in the HashMap, False
        if otherwise.  
        """
        index = self._hash_function(key) % self._buckets.length()
      
        # Iterate through the linked list at the appropriate index to determine whether or 
        # not it is in the HashMap.  
        node = self._buckets.get_at_index(index)
        for i in node:
            if i.key == key:
                return True
        
        return False

    def remove(self, key: str) -> None:
        """
        Takes as a parameter a key, and removes that key and associated value from
        the HashMap.  
        """
    
        index = self._hash_function(key) % self._buckets.length()
        # If the key is in the HashMap, remove it from the linked list at the appropriate index.  
        if self.contains_key(key):
            self._buckets.get_at_index(index).remove(key)
            self._size -= 1
        else:
            return
            
    def get_keys_and_values(self) -> DynamicArray:
        """
        Takes no parameters, and returns a DynamicArray where each index contains a 
        tuple of a key/value pair stored in the HashMap.  
        """
        da = DynamicArray()

        # If a bucket contains key/value pairs, iterate through each of them while adding a
        # tuple with their values to the DynamicArray.  
        for bucket in range(self._buckets.length()):
            if self._buckets.get_at_index(bucket).length() != 0:
                nodes = self._buckets.get_at_index(bucket)
                for node in nodes:
                    tup = (node.key, node.value)
                    da.append(tup)
        return da

def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Takes as a parameter a DynamicArray, and returns a tuple containing a 
    new DynamicArray comprising of the mode(s) of the initial array, and 
    an integer representing the frequency of the mode(s).  
    """

    map = HashMap()
    return_da = DynamicArray()
    current_mode = 1

    # Add the values from the input DynamicArray as keys to the HashMap, 
    # with the values representing their frequency..  
    for i in range(da.length()):
        # If the key is already in the map, increment its value by 1.  
        if map.contains_key(str(da.get_at_index(i))):
            value = map.get(str(da.get_at_index(i)))
            map.remove(str(da.get_at_index(i)))
            map.put(str(da.get_at_index(i)), value+1)
            # Update the current mode if appropriate.  
            if value+1 > current_mode:
                current_mode = value+1
        # Otherwise add it to the map.  
        else:
            map.put(str(da.get_at_index(i)),1)

    
    # Iterate through the keys and values, append the return array with the key if its frequency is the mode.  
    for index in range(map.get_keys_and_values().length()):
        key = map.get_keys_and_values().get_at_index(index)[0]
        value = map.get_keys_and_values().get_at_index(index)[1]
        if value == current_mode:
            return_da.append(key)
    
    return(return_da, current_mode)
