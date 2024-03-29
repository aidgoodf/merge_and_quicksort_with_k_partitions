# -*- coding: utf-8 -*-
# Aidan Goodfellow


def merge_sort_plus(arr, k):
  # raise error if incorrect value is input for k
    if k < 2 or k > 4:
        raise ValueError("k must be between 2 and 4 inclusive")

  # return array if length is 1 or is empty
    if len(arr) <= 1:
        return arr

    # Split the array into k equal parts
    split_size = len(arr) // k
    splits = [arr[i * split_size: (i + 1) * split_size] for i in range(k)]

    # if the array cannot be split into equal parts, add remaining elements from the end of the array to first splits one element at a time
    if len(arr) % k != 0:
        for i in range(len(arr) % k):
            splits[i].append(arr[-(i + 1)])

    # Recursively sort each split
    sorted_splits = [merge_sort_plus(split, k) for split in splits]

    # Merge the sorted splits
    return merge_sorted_arrays(sorted_splits)


# helper function to merge the partial arrays after they are sorted
def merge_sorted_arrays(sorted_arrays):
    result = []
    pointers = [0] * len(sorted_arrays)

    # while loop to add the smallest value to the result array for each value in the smaller sorted arrays
    while True:
      # set min value to infinity and min index to -1
        min_val = float('inf')
        min_idx = -1


        for i in range(len(sorted_arrays)):
            if pointers[i] < len(sorted_arrays[i]) and sorted_arrays[i][pointers[i]] < min_val:
                min_val = sorted_arrays[i][pointers[i]]
                min_idx = i

        if min_idx == -1:
            break

        result.append(min_val)
        pointers[min_idx] += 1

    return result

"""## k Random QS """

import random

# soort pivots manually because we can't use built in functions
def sort_pivots(pivots):
    if len(pivots) == 2:
        if pivots[0] > pivots[1]:
            pivots[0], pivots[1] = pivots[1], pivots[0]
    elif len(pivots) == 3:
        if pivots[0] > pivots[1]:
            pivots[0], pivots[1] = pivots[1], pivots[0]
        if pivots[1] > pivots[2]:
            pivots[1], pivots[2] = pivots[2], pivots[1]
        if pivots[0] > pivots[1]:
            pivots[0], pivots[1] = pivots[1], pivots[0]
    return pivots

def random_qs_plus(arr, k):
  # raise error if k is smaller than 2 or larger than 4
    if k < 2 or k > 4:
        raise ValueError("k must be between 2 and 4 inclusive")

    # return array if length is 1 or empty
    if len(arr) <= 1:
        return arr

    # Select k-1 random pivots and sort them manually, use length of set if k-1 is larger than the number of elements in the array
    # I sample from a set created from the array so the pivot values are unique
    num_pivots = min(len(set(arr)), k-1)
    pivots = sort_pivots(random.sample(set(arr), num_pivots))

    # Create partitions based on the pivots
    partitions = [[] for _ in range(k)]

    # if all of the values of the array are equal, we will distribute them among our partition choices.
    # before making this change I was getting recursion errors due to the recursion going too deep
    all_equal = True
    for num in arr:
        if num != arr[0]:
            all_equal = False
            break

    if all_equal:
        # Distribute equal elements across all partitions
        for i, num in enumerate(arr):
            partitions[i % k].append(num)
    else:

      for num in arr:
        #for i in range(k):
            #if i == k-1 or num <= pivots[i]:
                #partitions[i].append(num)
                #break
        if k == 2:
          if num <= pivots[0]:
            partitions[0].append(num)
          else:
            partitions[1].append(num)
        elif k == 3:
          if num <= pivots[0]:
            partitions[0].append(num)
          elif (num <= pivots[1]):
            partitions[1].append(num)
          else:
            partitions[2].append(num)
        elif k == 4:
          if num <= pivots[0]:
            partitions[0].append(num)
          elif num <= pivots[1]:
            partitions[1].append(num)
          elif num <= pivots[2]:
            partitions[2].append(num)
          else:
            partitions[3].append(num)


    # Recursively sort each partition
    sorted_partitions = [random_qs_plus(part, k) for part in partitions]

    # Concatenate the sorted partitions
    return sum(sorted_partitions, [])

"""## Benchmarking"""

import time
import matplotlib.pyplot as plt

def benchmark(func, max_size=10000, step=200):
    times = {2: [], 3: [], 4: []}
    sizes = list(range(step, max_size + 1, step))

    for size in sizes:
        arr = [random.randint(1, 1000) for _ in range(size)]
        for k in [2, 3, 4]:
            start_time = time.time()
            func(arr.copy(), k)
            elapsed_time = time.time() - start_time
            times[k].append(elapsed_time)

    return times, sizes

# Benchmarking
merge_sort_times, sizes = benchmark(merge_sort_plus, 10000, 200)
random_qs_times, _ = benchmark(random_qs_plus, 10000, 200)

# Plotting
plt.figure(figsize=(12, 6))

for k in [2, 3, 4]:
    plt.plot(sizes, merge_sort_times[k], label=f"Merge Sort (k={k})")
    plt.plot(sizes, random_qs_times[k], label=f"Randomized Quick Sort (k={k})", linestyle='--')

plt.xlabel("Array Size")
plt.ylabel("Time (seconds)")
plt.title("Performance of Sorting Algorithms")
plt.legend()
plt.grid(True)
plt.show()

import numpy as np
import numpy.testing as npt
import unittest

class Test_Sorting_Methods(unittest.TestCase):

    def test1(self):
        testarray = [random.randint(1, 1000) for _ in range(1000)]
        sorted_test = sorted(testarray)
        npt.assert_array_equal(merge_sort_plus(testarray, 2), sorted(testarray), "arrays are not equal")

    def test2(self):
        testarray2 = [random.randint(1, 1000) for _ in range(1000)]
        sorted_test = sorted(testarray2)
        npt.assert_array_equal(merge_sort_plus(testarray2, 3), sorted(testarray2), "arrays are not equal")

    def test3(self):
        testarray3 = [random.randint(1, 1000) for _ in range(1000)]
        sorted_test = sorted(testarray3)
        npt.assert_array_equal(merge_sort_plus(testarray3, 4), sorted(testarray3), "arrays are not equal")

    def test4(self):
        testarray4 = [random.randint(1, 1000) for _ in range(1000)]
        sorted_test = sorted(testarray4)
        npt.assert_array_equal(random_qs_plus(testarray4, 2), sorted(testarray4), "arrays are not equal")

    def test5(self):
        testarray5 = [random.randint(1, 1000) for _ in range(1000)]
        sorted_test = sorted(testarray5)
        npt.assert_array_equal(random_qs_plus(testarray5, 2), sorted(testarray5), "arrays are not equal")

    def test6(self):
        testarray6 = [random.randint(1, 1000) for _ in range(1000)]
        sorted_test = sorted(testarray6)
        npt.assert_array_equal(random_qs_plus(testarray6, 2), sorted(testarray6), "arrays are not equal")

for x in range(10):
    Test_Sorting_Methods.test1(unittest.TestCase)
    Test_Sorting_Methods.test2(unittest.TestCase)
    Test_Sorting_Methods.test3(unittest.TestCase)
    Test_Sorting_Methods.test4(unittest.TestCase)
    Test_Sorting_Methods.test5(unittest.TestCase)
    Test_Sorting_Methods.test6(unittest.TestCase)
