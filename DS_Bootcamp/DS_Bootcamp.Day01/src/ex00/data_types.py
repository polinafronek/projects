def data_types():
    digit = 8 
    string = "Data Science"
    value = 5.8 
    data = True 
    numbers = [1, 2, 3]
    dictionary = {"name": "Polina", "age": 18}
    tup = ("School", 21)
    sett = {1, 2 , 3, 4}
    array = [digit, string, value, data, numbers, dictionary, tup, sett]
    types = [type(x) for x in array]
    print([t.__name__ for t in types])

if __name__ == '__main__':
    data_types()
