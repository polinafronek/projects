from functools import reduce
import sys
import timeit

def loop(digit):
    sum = 0
    for i in range(digit + 1):
        sum = sum + i*i
    return sum

def reduce_func(digit):
    result = reduce(lambda x, y: x + y*y, range(digit + 1))
    return result

def main():
    if len(sys.argv) != 4:
        sys.exit()

    func = sys.argv[1]
    count = int(sys.argv[2])
    digit = int(sys.argv[3])
    if func == "loop":
        print(timeit.timeit(lambda: loop(digit), number=count))
    elif func == "reduce":
        print(timeit.timeit(lambda: reduce_func(digit), number=count))
    else:
        sys.exit()

if __name__ == "__main__":
    main()
