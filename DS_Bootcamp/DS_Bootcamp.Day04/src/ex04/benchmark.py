from random import randint
from collections import Counter
import timeit

def my_function(digits):
    counter = dict()
    for digit in digits:
        if digit not in counter.keys():
            counter[digit] = 1
        else:
            counter[digit] += 1
    return counter

def my_top(digits):
    counter = {}
    for digit in digits:
        if digit not in counter.keys():
            counter[digit] = 1
        else:
            counter[digit] += 1
    result = sorted(counter.items(), key=lambda x: -x[1])[:10]
    res_dict = {}
    for res in result:
        res_dict[res[0]] = res[1]
    return res_dict

def Counter_func(digits):
    counter = Counter(digits)
    return counter 

def Counter_top(digits):
    counter = Counter(digits)
    result = sorted(counter.items(), key=lambda x: -x[1])[:10]
    res_dict = {}
    for res in result:
        res_dict[res[0]] = res[1]
    return res_dict

def main():
    digits = [randint(0, 100) for i in range(1000000)]
    time_my_finction = timeit.timeit(lambda: my_function(digits), number=1)
    time_my_top = timeit.timeit(lambda: my_top(digits), number=1)
    time_Counter_func = timeit.timeit(lambda: Counter_func(digits), number=1)
    time_Counter_top = timeit.timeit(lambda: Counter_top(digits), number=1)
 
    print(f"my function: {time_my_finction}")
    print(f"Counter: {time_Counter_func}")
    print(f"my top: {time_my_top}")
    print(f"Counter's top: {time_Counter_top}")

if __name__ == "__main__":
    main()


