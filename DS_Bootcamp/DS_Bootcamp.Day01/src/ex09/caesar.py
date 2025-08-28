import sys

def encode(string, digit):
    string = string.split()

    new_string = []
    for word in string:
        current_array = []
        for x in word:
            if x.isalpha():
                shift = ord(x) + int(digit)
                if x.islower():
                    if shift > ord("z"):
                        shift -= 26
                    elif shift < ord("a"):
                        shift += 26
                else:
                    if shift > ord("Z"):
                        shift -= 26
                    elif shift < ord("A"):
                        shift += 26
                current_array.append(chr(shift))
            else:
                current_array.append(x)
        new_string.append("".join(current_array))

    print(" ".join(new_string))


def decode(string, digit):
    string = string.split()

    new_string = []
    for word in string:
        current_array = []
        for x in word:
            if x.isalpha():
                shift = ord(x) - int(digit)
                if x.islower():
                    if shift > ord("z"):
                        shift -= 26
                    elif shift < ord("a"):
                        shift += 26
                else:
                    if shift > ord("Z"):
                        shift -= 26
                    elif shift < ord("A"):
                        shift += 26
                current_array.append(chr(shift))
            else:
                current_array.append(x)
        new_string.append("".join(current_array))

    print(" ".join(new_string))


def main():
    if len(sys.argv) != 4 or sys.argv[1] not in ["encode", "decode"] or sys.argv[3].isdigit() == False:
        sys.exit(1)

    string = sys.argv[2]
    mode = sys.argv[1]
    digit = sys.argv[3]

    if mode == "encode":
        encode(string, digit)
    else:
        decode(string, digit)

if __name__ == "__main__":
    main()
