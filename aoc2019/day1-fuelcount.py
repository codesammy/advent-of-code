from util import read_file

lines = read_file()

fuel = 0

def fuel1(mass):
    return int(mass / 3) - 2

def fuel2(mass):
    def fuel_cost(total, mass):
        temp_fuel = int(mass / 3) - 2
        if temp_fuel < 0:
            return total
        return fuel_cost(total+temp_fuel, temp_fuel)
    
    return fuel_cost(0, mass)

for line in lines:
    mass = int(line)
    current_fuel = fuel2(mass)
    fuel += current_fuel

assert fuel1(14) == 2
assert fuel2(1969) == 966

print("final fuel = " + str(fuel))

