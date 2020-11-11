import functools
import math
import random
import time
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Tuple, Union


def timer(func: Callable) -> Callable:
    """
    Timer decorator which measures time execution and returns cycles count from function
    :param func: Basically, sort function
    :return: return function wrapper, which return time and memory
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        memory = func(*args, **kwargs)
        end = time.perf_counter()
        period = end - start
        return period, memory

    return wrapper


class Algorithm(ABC):
    """
    Abstract algorithm class
    """

    def __init__(self, lowerBound: int, upperBound: int, maxSize: int) -> None:
        self.maxSize = maxSize
        self.lowerBound = lowerBound
        self.upperBound = upperBound

    def generateArray(self, size: Optional[int] = None) -> List[int]:
        """
        Generate max sized or given sized array of integers in bounds
        :param size: Size of array
        :return: list of random integers
        """
        if size is None:
            return [random.randrange(self.lowerBound, self.upperBound) for _ in range(self.maxSize)]
        else:
            return [random.randrange(self.lowerBound, self.upperBound) for _ in range(size)]

    def formatMeasurements(self, period: float, size: int, memory: int) -> Dict[str, str]:
        """
        Format all measurements into dict
        :param period: Time delta of algorithm execution
        :param size: Size of array
        :param memory: Amount of cycles executed
        :return: Dict of measurements
        """
        return {
            "size": f"{size}",
            "calculated_time": f"{period * 1000000:.2f}",
            "estimated_time": f"{self.analyticalTime(size)}",
            "memory": f"{memory}"
        }

    def calculate(self) -> Dict[str, List[str]]:
        """
        Calculates from 1 to MaxSize records for more accuracy
        :return: Dict of calculated records
        """
        data = {
            "size": [],
            "calculated_time": [],
            "estimated_time": [],
            "memory": []
        }
        for size in range(1, self.maxSize):
            # Iterates for every size and creates records
            array = self.generateArray(size)
            period, memory = self.sort(array)
            for key, value in self.formatMeasurements(period, size, memory).items():
                data[key].append(value)

        return data

    @abstractmethod
    def sort(self, array: List[int]) -> int:
        """
        Implement sorting algorithm, which mutating and sorting array.
        :param array: List of random integers
        :return: Amount of cycles counted
        """
        pass

    @abstractmethod
    def analyticalTime(self, n) -> int:
        """
        Implement average O(n) analytical time
        For example, Bubble Sort: O(n^2)
        :param n: Size of array
        :return: Analytical time complexity
        """
        pass

    @abstractmethod
    def __repr__(self):
        pass


class BubbleSort(Algorithm):
    """
    Bubble sort algorithm

    Bubble sort is a sorting algorithm that works by repeatedly stepping through
    lists that need to be sorted, comparing each pair of adjacent items and swapping
    them if they are in the wrong order. This passing procedure is repeated until no swaps are
    required, indicating that the list is sorted

    Worst case: O(n^2)
    Average case: O(n^2)
    Best case: O(n) or O(1)
    """

    @timer
    def sort(self, array):
        has_swapped = True
        count = 0

        while has_swapped:
            has_swapped = False
            for i in range(len(array) - 1):
                count += 1
                if array[i] > array[i + 1]:
                    array[i], array[i + 1] = array[i + 1], array[i]
                    has_swapped = True
        return count

    def analyticalTime(self, n):
        return n ** 2

    def __repr__(self):
        return "Sortowanie bąbelkowe (Bubble sort)"


class InsertionSort(Algorithm):
    """
    Insertion sort algorithm

    Insertion sort iterates, consuming one input element each repetition,
    and growing a sorted output list. At each iteration, insertion sort removes
    one element from the input data, finds the location it belongs within the sorted list,
    and inserts it there. It repeats until no input elements remain

    Worst case: O(n^2)
    Average case: O(n^2)
    Best case: O(n) or O(1)
    """

    @timer
    def sort(self, array):
        count = self.insertionSort(array)
        return count

    def analyticalTime(self, n):
        return n ** 2

    def insertionSort(self, array: List[int]) -> int:
        """
        Implementation of "sort" method, instead of implementing directly in abstract
        class, for make it possible to Inherit as a parent for Bucket Sort,
        which use Insertion algorithm

        :param array: Array of random integers
        :return: Amount of cycles executed
        """
        count = 0
        for index in range(1, len(array)):
            currentValue = array[index]
            currentIndex = index

            while currentIndex > 0 and array[currentIndex - 1] > currentValue:
                array[currentIndex] = array[currentIndex - 1]
                currentIndex -= 1
                count += 1
            else:
                count += 1

            array[currentIndex] = currentValue
        return count

    def __repr__(self):
        return "Sortowanie wstaweniem (Insertion sort)"


class BucketSort(InsertionSort):
    """
    Bucket sort algorithm

    Its inherits from Insertions sort to use sorting under buckets

    Bucket sort, or bin sort, is a sorting algorithm that works by distributing
    the elements of an array into a number of buckets.
    Each bucket is then sorted individually, either using a different sorting algorithm,
    or by recursively applying the bucket sorting algorithm

    Worst case: O(n^2)
    Average case: O(n + n^2 / k + k) where k is number of buckets
                  O(n) if n ~= k
    """

    @timer
    def sort(self, array):
        maxValue = max(array)
        size = maxValue / len(array)
        count = 0

        buckets = []
        for _ in array:
            buckets.append([])
            count += 1

        for index in range(len(array)):
            el = int(array[index] / size)
            count += 1
            if el != len(array):
                buckets[el].append(array[index])
            else:
                buckets[len(array) - 1].append(array[index])

        for index in range(len(array)):
            count += self.insertionSort(buckets[index]) + 1

        return count

    def analyticalTime(self, n):
        return n

    def __repr__(self):
        return "Sortowanie kubełkowe (Bucket sort)"


class QuickSort(Algorithm):
    """
    Quick sort algorithm

    Quicksort is a divide-and-conquer algorithm. It works by selecting a 'pivot' element
    from the array and partitioning the other elements into two sub-arrays,
    according to whether they are less than or greater than the pivot.
    The sub-arrays are then sorted recursively.

    Worst case: O(n^2)
    Average case: O(n*log n)
    Best case: O(n*log n) or O(n)
    """

    @timer
    def sort(self, array: List[int]) -> int:
        count = self.quickSort(array, 0, len(array) - 1, 0)
        return count

    def quickSort(self, array: List[int], start: int, end: int, count: int) -> int:
        if start >= end:
            return count

        p, pCount = self.partition(array, start, end)
        count += pCount + 1
        count = self.quickSort(array, start, p - 1, count)
        count = self.quickSort(array, p + 1, end, count)

    def partition(self, array: List[int], start: int, end: int) -> Tuple[Union[int, Any], int]:
        pivot = array[start]
        low = start + 1
        high = end
        count = 0

        while True:
            count += 1
            # If the current value we're looking at is larger than the pivot
            # it's in the right place (right side of pivot) and we can move left,
            # to the next element.
            # We also need to make sure we haven't surpassed the low pointer, since that
            # indicates we have already moved all the elements to their correct side of the pivot
            while low <= high and array[high] >= pivot:
                high = high - 1
                count += 1

            # Opposite process of the one above
            while low <= high and array[low] <= pivot:
                low = low + 1
                count += 1

            # We either found a value for both high and low that is out of order
            # or low is higher than high, in which case we exit the loop
            if low <= high:
                array[low], array[high] = array[high], array[low]
                # The loop continues
            else:
                # We exit out of the loop
                break

        array[start], array[high] = array[high], array[start]

        return high, count

    def analyticalTime(self, n):
        return n * math.log(n, 10)

    def __repr__(self):
        return "Szybkie sortowanie (Quick sort)"


# test = QuickSort(10, 100, 50)
# # print(test.sort(test.generateArray()))
# print(test.calculate())
