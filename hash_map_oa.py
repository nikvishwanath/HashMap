# HashMap - Open Addressing Implementation

from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        # Must resize if load factor >= 0.5.
        if self.table_load() >= 0.5:
            self.resize_table(self.get_capacity()*2)
       
        # To be added.
        entry = HashEntry(key, value)
        # Initial index
        index = self._hash_function(key) % self._buckets.length()

        # First check to see if the key already exists in the HashMap.  If it does,
        # update it and return. 
        if self.contains_key(key):
            j = 1
            new_index = index
            while self._buckets.get_at_index(new_index).key != key:
                new_index = (index + j**2) % self._buckets.length()
                j += 1
            self._buckets.set_at_index(new_index, entry)
            return

        # If initial index is empty or contains a tombstone.  
        if self._buckets.get_at_index(index) is None or self._buckets.get_at_index(index).is_tombstone is True:
            self._buckets.set_at_index(index, entry)
            self._size += 1
            return
        
        # Otherwise probing is required.  
        else:
            j = 1
            new_index = (index + j**2) % self._buckets.length()
            # Probe until insertion.  
            while self._buckets.get_at_index(new_index) is not None and self._buckets.get_at_index(new_index).is_tombstone is False:
                j += 1
                new_index = (index + j**2) % self._buckets.length()
            # Insert once an empty bucket or tombstone is reached.    
            self._buckets.set_at_index(new_index, entry)
            self._size += 1
            return

    def table_load(self) -> float:
        """
        Takes no parameters, and returns the load factor of the HashMap.
        """
        return self.get_size() / self.get_capacity()

    def empty_buckets(self) -> int:
        """
        Takes no parameters, and returns the number of empty buckets in the HashMap.  
        """
        return self.get_capacity() - self.get_size()
         
    def resize_table(self, new_capacity: int) -> None:
        """
        Takes as a parameter a new capacity, and resizes the HashMap to that capacity. 
        """
        array_capacity = None

        # Do nothing with capacity less than the current size.   
        if new_capacity < self.get_size():
            return
        # Otherwise make sure that the new capacity is a prime number.  
        if self._is_prime(new_capacity):
            array_capacity = new_capacity
        else:
            next_prime = self._next_prime(new_capacity)
            array_capacity = next_prime
    
        # Update the capacity. 
        self._capacity = array_capacity
        
        # Store old array.  
        old_da = self._buckets

        # DynamicArray with new capacity.  
        da = DynamicArray()
        for i in range(array_capacity):
            da.append(None)
        
        # Reassign to new DynamicArray.     
        self._buckets = da
        self._size = 0

        # Add in data from old array, removing tombstones.    
        for i in range(old_da.length()):
            if old_da.get_at_index(i) and old_da.get_at_index(i).is_tombstone is False:
                self.put(old_da.get_at_index(i).key, old_da.get_at_index(i).value)
                
    def get(self, key: str) -> object:
        """
        Takes as a paramter a key, and returns the associated value.  
        """
        # If the key is not in the HashMap.  
        if self.contains_key(key) is False:
            return None
        
        # Otherwise, start at the index generated by the hash function, and 
        # probe until the key is located, then return the value.   
        else:
            index = self._hash_function(key) % self._buckets.length()
            new_index = index
            j = 1
            while self._buckets.get_at_index(new_index).key != key:
                new_index = (index + j**2) % self._buckets.length()
                j += 1            
            
            return self._buckets.get_at_index(new_index).value 
        
    def contains_key(self, key: str) -> bool:
        """
        Takes as a parameter a key, and returns True if the key is in the HashMap, False
        if otherwise. 
        """
        initial_index = self._hash_function(key) % self._buckets.length()

        # If the initial index is empty, the key is not in the HashMap. 
        if self._buckets.get_at_index(initial_index) is None:
            return False
        # If the initial index contains the key and is not a tombstone, the key is in the HashMap.  
        elif self._buckets.get_at_index(initial_index).key == key and self._buckets.get_at_index(initial_index).is_tombstone is False:
            return True
        # Otherwise, probe until arriving at an empty bucket, at which point the key is not in the HashMap.  
        else:
            j = 1
            new_index = (initial_index + j**2) % self._buckets.length()
            while self._buckets.get_at_index(new_index):
                if self._buckets.get_at_index(new_index).key == key and self._buckets.get_at_index(new_index).is_tombstone is False:
                    return True
                else:
                    j += 1
                    new_index = (initial_index + j**2) % self._buckets.length()

        return False

    def remove(self, key: str) -> None:
        """
        Takes as a parameter a key, and removes that key and associated value from
        the HashMap. 
        """
        # If the HashMap doesn't contain the key. 
        if self.contains_key(key) is False:
            return
        # Otherwise, start at the index generated by the hash function, and probe until the key 
        # is reached.   
        j = 1
        initial_index = self._hash_function(key) % self._buckets.length()
        new_index = initial_index
        while self._buckets.get_at_index(new_index).key != key:
            new_index = (initial_index + j**2) % self._buckets.length()
            j += 1
        # Change it to a tombstone, and decrease the size of the HashMap by 1.  
        self._buckets.get_at_index(new_index).is_tombstone = True
        self._size -= 1
        return 
    def clear(self) -> None:
        """
        Takes no parameters, and clears the contents of the HashMap.
        """
        da = DynamicArray()
        for i in range(self.get_capacity()):
            da.append(None)
        self._buckets = da
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Takes no parameters, and returns a DynamicArray where each index contains a 
        tuple of a key/value pair stored in the HashMap.
        """
        da = DynamicArray()

        # Iterate through the HashMap, appending a tuple containing the key/value pair at each bucket to the return array..  
        for i in range(self._buckets.length()):
            if self._buckets.get_at_index(i) and self._buckets.get_at_index(i).is_tombstone is False:
                tup = (self._buckets.get_at_index(i).key, self._buckets.get_at_index(i).value)
                da.append(tup)
        
        return da

