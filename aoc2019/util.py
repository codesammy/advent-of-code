def read_file():
    inputfile = open("input.txt", "r")
    lines = inputfile.readlines()
    inputfile.close()
    return lines
