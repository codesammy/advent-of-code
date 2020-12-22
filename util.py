def read_file(filename="input.txt"):
    inputfile = open(filename, "r")
    lines = inputfile.readlines()
    inputfile.close()
    return [x.strip() for x in lines]

def read_file_one_string(filename="input.txt"):
    inputfile = open(filename, "r")
    res = inputfile.read()
    inputfile.close()
    return res

def assert_equals(actual, expected):
    if (actual != expected):
        raise(Exception("%s was not %s" % (actual, expected)))
