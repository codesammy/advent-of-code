import sys
import math
import re
sys.path.append('../')

from util import read_file, assert_equals


class Passport:
    keyvalue_pattern = re.compile("([^ :]+):([^ ]+)")
    hcl_pattern = re.compile("#[0-9a-f]{6}")
    hgt_pattern = re.compile("([0-9]+)([^0-9]+)")
    pid_pattern = re.compile("[0-9]{9}")

    def apply(self, line):
        for key, value in self.keyvalue_pattern.findall(line):
            setattr(self, key, value)

    def attribute_count(self):
        count = 0
        for f in ['byr','iyr','eyr','hgt','hcl','ecl','pid', 'cid']:
            if hasattr(self, f):
                count += 1
        return count

    def is_valid1(self):
        for f in ['byr','iyr','eyr','hgt','hcl','ecl','pid']:
            if hasattr(self, f) == False:
                return False
        return True

    def is_valid2(self):
        if not self.is_valid1():
            return False
        if not (int(self.byr) >= 1920 and int(self.byr) <= 2002):
            return False
        if not (int(self.iyr) >= 2010 and int(self.iyr) <= 2020):
            return False
        if not (int(self.eyr) >= 2020 and int(self.eyr) <= 2030):
            return False
        if not self.hcl_pattern.fullmatch(self.hcl):
            return False
        m = self.hgt_pattern.fullmatch(self.hgt)
        if m == None:
            return False
        else:
            hgt, unit = m.groups()
            hgt = int(hgt)
            if unit == "cm":
                if not (hgt >= 150 and hgt <= 193):
                    return False
            if unit == "in":
                if not (hgt >= 59 and hgt <= 76):
                    return False
        ecl = ['amb','blu','brn','gry','grn','hzl','oth']
        if self.ecl not in ecl:
            return False
        if not self.pid_pattern.fullmatch(self.pid):
            return False
        return True

    def __str__(self):
        return "Passport["+",".join(map(lambda x: x + ":" + getattr(self,x) if hasattr(self, x) else "<missing>",['byr','iyr','eyr','hgt','hcl','ecl','pid','cid']))+"]"

def parse_passports(lines):
    passports = []
    p = Passport()
    passports.append(p)
    for line in lines:
        if line == "":
            p = Passport()
            passports.append(p)
        else:
            p.apply(line)
    return passports

def part1(lines):
    passports = parse_passports(lines)
    return sum(1 for p in passports if p.is_valid1())

def part2(lines):
    passports = parse_passports(lines)
    return sum(1 for p in passports if p.is_valid2())

sample = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in""".split("\n")
assert_equals(part1(sample), 2)

sample_invalid = """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007""".split("\n")
assert_equals(part2(sample_invalid), 0)

sample_valid = """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719""".split("\n")
assert_equals(part2(sample_valid), 4)

lines = read_file(sys.argv[0].replace("py", "input"))
print(part1(lines))
print(part2(lines))
