def read_file(filename="input.txt"):
    inputfile = open(filename, "r")
    lines = inputfile.readlines()
    inputfile.close()
    return lines

def assert_equals(actual, expected):
    if (actual != expected):
        raise(Exception("%s was not %s" % (actual, expected)))
