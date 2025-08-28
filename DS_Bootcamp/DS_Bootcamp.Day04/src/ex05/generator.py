import sys
import resource

def reading_file(path):
    data_from_path = []
    with open(path, "r", encoding="utf-8") as file_in:
        for line in file_in:
            yield line
            data_from_path.append(line)

    return data_from_path

def main():
    if len(sys.argv) != 2:
        sys.exit()

    path = sys.argv[1]
    result = reading_file(path)

    memory = resource.getrusage(resource.RUSAGE_SELF)

    memory_GB = round((memory.ru_maxrss) / (2 ** 30), 3)
    user_time = memory.ru_utime
    system_time = memory.ru_stime

    print(f"Peak Memory Usage = {memory_GB} GB")
    print(f"User Mode Time + System Mode Time = {round(user_time + system_time, 2)}s")
 
if __name__ == "__main__":
    main()