
lines = ['h,tail\n', '0,1\n', '1,    0\n', '0,1\n', '1,0\n', '0,1\n', '0,1\n', '0,1\n', '1,0\n', '1,0\n', '0,1\n', '1,0\n', '0,1\n']
lines = [lines[i].strip().split(",") for i in range(len(lines))] 

for line in lines:
    print(line)