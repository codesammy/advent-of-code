from util import read_file

lines = read_file()

def parse(state_desc):
    return list(map(int, state_desc.split(",")))

def run(state):
    def op(opcode, a, b):
        if opcode == 1:
            return a + b
        if opcode == 2:
            return a * b
    def run_at_pos(pos):
        opcode = state[pos]
        if (opcode == 99):
            return
        operand1 = state[state[pos+1]]
        operand2 = state[state[pos+2]]
        state[state[pos+3]] = op(opcode, operand1, operand2)
        run_at_pos(pos + 4)
    run_at_pos(0)
    return state[0];

assert run(parse("1,9,10,3,2,3,11,0,99,30,40,50")) == 3500

state = parse(lines[0])

def run_noun_verb(noun, verb):
    clean_state = list(state)
    clean_state[1] = noun
    clean_state[2] = verb
    return run(clean_state)

for noun in range(100):
    for verb in range(100):
        result = run_noun_verb(noun, verb)
        if result == 19690720:
            print("noun = " + str(noun) + " " + "verb = " + str(verb) + " " + "result = " + str(result))
            print("100*noun+verb = " + str(100*noun+verb))
            break

# part one
print(str(run_noun_verb(12, 2)))
