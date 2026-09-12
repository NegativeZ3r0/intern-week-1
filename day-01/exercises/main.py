from collections import Counter, deque


def reverse_string(text: str) -> str:
    reversed_text = ""
    for char in text:
        reversed_text = char + reversed_text
    return reversed_text


def is_palindrome(text: str) -> bool:
    return text == text[::-1]


def get_second_largest(numbers: list[int]) -> int:
    unique_numbers = set(numbers)
    if len(unique_numbers) < 2:
        raise ValueError("List must contain at least two distinct numbers.")
    unique_numbers.remove(max(unique_numbers))
    return max(unique_numbers)


def remove_duplicates(numbers: list[int]) -> set[int]:
    return set(numbers)


def find_missing_number(numbers: list[int]) -> int:
    n = len(numbers) + 1
    expected_sum = (n * (n + 1)) // 2
    actual_sum = sum(numbers)
    return expected_sum - actual_sum


def get_character_frequency(text: str) -> dict[str, int]:
    return dict(Counter(text))


def first_unique_char(text):
    counts = Counter(text)  # Creates a dictionary of character frequencies

    for char in text:
        if counts[char] == 1:
            return char  # Returns the very first character with a count of 1

    return None  # Returns None if all characters repeat


def merge_sorted_arrays(arr1, arr2):
    merged = []
    i, j = 0, 0  # Pointers for arr1 and arr2

    # Compare elements from both arrays and add the smaller one
    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            merged.append(arr1[i])
            i += 1
        else:
            merged.append(arr2[j])
            j += 1

    # Append any remaining elements left over in arr1 or arr2
    merged.extend(arr1[i:])
    merged.extend(arr2[j:])

    return merged


def find_common_element(list1, list2):

    # Find the intersection
    common = list(set(list1) & set(list2))

    return common  # Output: [2, 4]


class Stack:

    def __init__(self):
        self._items = []

    def push(self, value):
        self._items.append(value)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        """Look at the top item without removing it."""
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def size(self) -> int:
        return len(self._items)

    def all_values(self) -> list:
        # Return a shallow copy to prevent external mutation of internal state
        return self._items.copy()


class Queue:

    def __init__(self):
        # deque provides O(1) pops from the left side, unlike list.pop(0) which is O(n)
        self._items = deque()

    def enqueue(self, value):
        self._items.append(value)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._items.popleft()

    def peek(self):
        """Look at the front item without removing it."""
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self._items[0]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def size(self) -> int:
        return len(self._items)

    def all_values(self) -> list:
        # Return a copy as a standard list
        return list(self._items)


def max_subarray_sum(nums):
    # Initialize both tracking variables with the first element
    max_so_far = nums[0]
    current_max = nums[0]

    # Loop through the rest of the array starting from the second element
    for num in nums[1:]:
        # Decide whether to add the current number to the existing subarray,
        # or start a brand new subarray from the current number
        current_max = max(num, current_max + num)

        # Update the absolute highest sum found so far
        max_so_far = max(max_so_far, current_max)

    return max_so_far


def quick_sort(arr):
    # Base case: arrays with 0 or 1 element are already sorted
    if len(arr) <= 1:
        return arr

    # Choose the middle element as the pivot
    pivot = arr[len(arr) // 2]

    # Partition the array into three groups
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    # Recursively sort left and right, then combine them
    return quick_sort(left) + middle + quick_sort(right)

def is_anagram(str1: str, str2: str) -> bool:
    # Remove spaces and convert to lowercase for a fair comparison
    clean_str1 = str1.replace(" ", "").lower()
    clean_str2 = str2.replace(" ", "").lower()

    # Anagrams must have the exact same character frequencies
    return Counter(clean_str1) == Counter(clean_str2)


def two_sum(nums: list[int], target: int) -> list[int]:
    # Dictionary to store: {number_value: index_position}
    seen = {}

    for current_index, num in enumerate(nums):
        complement = target - num

        # If the complement exists in the dictionary, we found our pair
        if complement in seen:
            return [seen[complement], current_index]

        # Otherwise, save the current number and its index to the dictionary
        seen[num] = current_index

    return []  # Return empty list if no pair is found

if __name__ == "__main__":

    # 1. Reverse a string
    sample_text = "Python"
    reversed_result = reverse_string(sample_text)
    print(f"1. text: {sample_text}, reversed: {reversed_result}", end='\n')


    # 2. Palindrome check
    word = "radar"
    print(f"2. is word '{word}' a palindrome? {is_palindrome(word)}", end='\n')


    # 3. Second-largest number
    num_list = [10, 20, 40, 40, 30]
    print(f"3. numbers: {num_list}, Second largest number: {get_second_largest(num_list)}", end='\n')


    # 4. Remove duplicates
    print(f"4. numbers (list): {num_list}, without duplicates (set): {remove_duplicates(num_list)}", end='\n')


    # 5. Missing number
    consecutive_nums = [1, 2, 3, 5, 6]
    print(f"5. numbers: {consecutive_nums}, missing number: {find_missing_number(consecutive_nums)}", end='\n')


    # 6. Character frequency
    phrase = "hello world"
    print(f"6. phrase: '{phrase}', character frequency: {get_character_frequency(phrase)}", end='\n')


    # 7. first non-repeating character
    string = "aabbc"
    print(f"7. string: {string}, first non-repeating character: {first_unique_char(string)}", end='\n')


    # 8. merge sorted arrays
    list1 = [1, 3, 5, 7]
    list2 = [2, 4, 6, 8, 10]
    print(f"8. list1: {list1}, list2: {list2}, merged sorted array: {merge_sorted_arrays(list1, list2)}", end='\n')


    # 9. common element
    list1 = [1, 2, 2, 3, 4]
    list2 = [2, 2, 4, 5, 6]
    print(f"9. list1: {list1}, list2: {list2}, common elements: {find_common_element(list1, list2)}", end='\n')


    # 10. stack
    stack = Stack()
    stack.push('a')
    stack.push('b')
    print(f"10. stack: {stack.all_values()} pop: {stack.pop()}, pop: {stack.pop()}", end='\n')


    # 11. queue
    queue = Queue()
    queue.enqueue(1)
    queue.enqueue(2)
    print(f"11. queue: {queue.all_values()}, dequeue: {queue.dequeue()}, dequeue: {queue.dequeue()}", end='\n')


    # 12. maximum subarray sum
    numbers = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(f"12. numbers: {numbers}, maximum subarray sum: {max_subarray_sum(numbers)}", end='\n') # Output: 6
    # (The maximum subarray is [4, -1, 2, 1], which sums up to 6)


    # 13. sorting
    numbers = [3, 6, 8, 10, 1, 2, 1]
    print(f"13. numbers: {numbers}, sorted numbers: {quick_sort(numbers)}", end='\n')  # Output: [1, 1, 2, 3, 6, 8, 10]

    # 14. anagrams
    str1 = "listen"
    str2 = "silent"
    print(f"14. is 'listen' and 'silent' are anagrams of each other: {is_anagram(str1, str2)}", end='\n')

    # 15. two sum
    # Given an array of integers and a target number, find the indices of the two numbers that add up to that specific target.
    numbers = [3, 2, 4]
    target = 6
    print(f"15. numbers: {numbers}, target: {target}, indices of two numbers which add up to target: {two_sum(numbers, target)}", end='\n')
