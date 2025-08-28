def parsing_string(data):
    status = False
    new = []
    for char in data:
        if char == '"':
            status = not status
        elif char == "," and status == False:
            new.append("\t")
        else:
            new.append(char)
    return "".join(new)

def csv_to_tsv(input, output):       
    result = []
    with open(input, encoding="utf-8") as file_in:
        for line in file_in:
            result.append(parsing_string(line))

    with open(output, "w", encoding="utf-8") as file_out:
        file_out.writelines(result)

if __name__ == '__main__':
    csv_to_tsv("ds.csv", "ds.tsv")