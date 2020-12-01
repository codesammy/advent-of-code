import sys
sys.path.append('../')

from util import read_file, assert_equals

lines = read_file()

class Point:
    x = None
    y = None
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def to(self, direction, amount):
        return {"L":Point(self.x - amount, self.y),
         "U":Point(self.x, self.y + amount),
         "R":Point(self.x + amount, self.y),
         "D":Point(self.x, self.y - amount)}[direction]
    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)
    def origin_distance(self):
        return self.distance(Point(0, 0))
    def __str__(self):
        return "Point(%s,%s)" % (self.x , self.y)
    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
      return hash((self.x, self.y))
        
class Line:
    p1 = None
    p2 = None
    horizontal = False
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        if self.p1.y == self.p2.y:
            self.horizontal = True
    def intersects(self, other):
        if self.horizontal == other.horizontal:
            return None
        if self.horizontal:
            if (other.p1.x >= min(self.p1.x, self.p2.x)
                and other.p1.x <= max(self.p1.x, self.p2.x)
                and self.p1.y >= min(other.p1.y, other.p2.y)
                and self.p1.y <= max(other.p1.y, other.p2.y)):
                return Point(other.p1.x, self.p1.y)
            else:
                return None
        else:
            return other.intersects(self)
    def contains(self, point):
        if self.horizontal:
            return point.y == self.p1.y
        else:
            return point.x == self.p1.x
    def index(self, point):
        inc = 1
        if self.horizontal:
            if self.p1.x > self.p2.x:
                inc = -1
            for x in range(self.p1.x, self.p2.x + inc, inc):
                if Point(x, self.p1.y) == point:
                    return abs(self.p1.x - x)
        else:
            if self.p1.y > self.p2.y:
                inc = -1
            #print("%s -(%s)> %s" % (self.p1, inc, self.p2))
            for y in range(self.p1.y, self.p2.y + inc, inc):
                if Point(self.p1.x, y) == point:
                    return abs(self.p1.y - y)
    def __len__(self):
        if self.horizontal:
            return abs(self.p1.x - self.p2.x)
        else:
            return abs(self.p1.y - self.p2.y)
    def __str__(self):
        return "Line(%s,%s,%s)" % (self.p1, self.p2, self.horizontal)

class Wire:
    def __init__(self, input):
        commands = list(map(lambda x : (x[0], int(x[1:])),input.split(",")))
        point = Point(0, 0)
        self.lines = []
        for direction, amount in commands:
            new_point = point.to(direction, amount)
            self.lines.append(Line(point, new_point))
            point = new_point
    def lines(self):
        return self.lines
    def intersects(self, other):
        intersections = []
        for a in self.lines:
            for b in other.lines:
                point = a.intersects(b)
                if point and not point in intersections:
                    intersections.append(point)
        return intersections
    def count_steps(self, point):
        steps = 0
        for l in self.lines:
            #print("Line ===== %s" % l)
            if l.contains(point):
                #print("%s contains %s" % (l, point))
                #print("index = %s" % l.index(point))
                steps += l.index(point)
                break
            else:
                #print("len of %s is %s" % (l, len(l)))
                steps += len(l)
        return steps
        
def intersect_distance(lines_a, lines_b):
    intersections = lines_a.intersects(lines_b)
    intersections = [i for i in intersections if i != Point(0,0)]
    distances = map(lambda p : p.origin_distance(), intersections)
    return min(distances)

def minimal_signal_delay(wire1, wire2):
    delay = float('inf')
    intersections = wire1.intersects(wire2)
    intersections = [i for i in intersections if i != Point(0,0)]
    for i in intersections:
        #print("point %s" % i)
        temp_delay = wire1.count_steps(i) + wire2.count_steps(i)
        #print("temp delay = %s" % temp_delay)
        delay = min(delay, temp_delay)
    return delay

assert(Point(1,2).distance(Point(0,0)) == 3)
assert_equals(Line(Point(3,5),Point(3,2)).index(Point(3,3)), 2)

x = Line(Point(1,2), Point(5,2))
y = Line(Point(4,1), Point(4,5))
assert(x.intersects(y) == Point(4,2))
assert(len(x) == 4)

lines_a = Wire("R8,U5,L5,D3")
lines_b = Wire("U7,R6,D4,L4")
assert(intersect_distance(lines_a, lines_b) == 6)
assert_equals(lines_a.lines[0].contains(Point(7,0)), True)
assert_equals(lines_a.lines[0].index(Point(7,0)), 7)
assert_equals(lines_a.count_steps(Point(7,0)), 7)
assert_equals(minimal_signal_delay(lines_a, lines_b), 30)


lines_a = Wire("R75,D30,R83,U83,L12,D49,R71,U7,L72")
lines_b = Wire("U62,R66,U55,R34,D71,R55,D58,R83")
assert(intersect_distance(lines_a, lines_b) == 159)

lines_a = Wire("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51")
lines_b = Wire("U98,R91,D20,R16,D67,R40,U7,R15,U6,R7")
assert(intersect_distance(lines_a, lines_b) == 135)

lines_a = Wire("R993,U847,R868,D286,L665,D860,R823,U934,L341,U49,R762,D480,R899,D23,L273,D892,R43,U740,L940,U502,L361,U283,L852,D630,R384,D758,R655,D358,L751,U970,R72,D245,L188,D34,R355,U373,L786,U188,L304,D621,L956,D839,R607,U279,L459,U340,R412,D901,L929,U256,R495,D462,R369,D138,R926,D551,L343,U237,L434,U952,R421,U263,L663,D694,R687,D522,L47,U8,L399,D930,R928,U73,L581,U452,R80,U610,L998,D797,R584,U772,L521,U292,L959,U356,L940,D894,R774,U957,L813,D650,L891,U309,L254,D271,R791,D484,L399,U106,R463,D39,L210,D154,L380,U86,L136,D228,L284,D267,R195,D727,R739,D393,R395,U703,L385,U483,R433,U222,L945,D104,L605,D814,L656,U860,L474,D672,L812,U789,L29,D256,R857,U436,R927,U99,R171,D727,L244,D910,L347,U789,R49,U598,L218,D834,L574,U647,L185,U986,L273,D363,R848,U531,R837,U433,L795,U923,L182,D915,R367,D347,R867,U789,L776,U568,R969,U923,L765,D589,R772,U715,R38,D968,L845,D327,R721,D928,R267,U94,R763,U799,L946,U130,L649,U521,L569,D139,R584,D27,L823,D918,L450,D390,R149,U237,L696,U258,L757,U810,L216,U202,L966,U157,R702,D623,R740,D560,R932,D587,L197,D56,R695,U439,R655,U576,R695,D176,L800,D374,R806,U969,L664,U216,L170,D415,R485,U188,L444,D613,R728,U508,L644,U289,R831,D978,R711,U973,R3,U551,R377,U114,L15,U812,R210,D829,L536,D883,L843,D427,L311,D680,R482,D69,R125,D953,L896,D85,R376,D683,R374,U415,L3,U843,L802,D124,R299,U345,L696,D276,L87,D98,R619,D321,R348,D806,L789,U657,R590,D747,L477,U251,R854,D351,L82,D982,R906,D94,R285,U756,L737,D377,L951,U126,L852,D751,L946,U696,L44,D709,R851,D364,R222")
lines_b = Wire("L1002,D658,L695,U170,L117,U93,R700,D960,L631,U483,L640,D699,R865,U886,L59,D795,R265,U803,R705,D580,R519,U685,R126,D888,R498,U934,L980,U734,L91,D50,R805,U197,R730,U363,R337,U594,L666,U702,L237,D140,L72,U980,L167,U598,L726,U497,L340,D477,L304,U945,R956,U113,L43,D4,R890,D316,R916,D644,R704,D398,L905,U361,R420,U31,L317,U338,R703,D211,R27,D477,L746,U813,R705,U191,L504,D434,R697,D945,R835,D374,L512,U269,L299,U448,R715,U363,R266,U720,L611,U672,L509,D983,L21,U895,L340,D794,R528,U603,R154,D610,L582,U420,L696,U599,R16,U610,L134,D533,R156,D338,L761,U49,L335,D238,R146,U97,L997,U545,L896,D855,L653,D789,R516,D371,L99,D731,R868,D182,R535,D35,R190,D618,R10,D694,L567,D17,R356,U820,R671,D883,R807,U218,L738,U225,L145,D954,R588,U505,R108,U178,R993,D788,R302,D951,R697,D576,L324,U930,R248,D245,R622,U323,R667,U876,L987,D411,L989,U915,R157,D67,L968,U61,R274,D189,L53,D133,R617,D958,L379,U563,L448,D412,R940,U12,R885,U121,R746,U215,R420,U346,L469,D839,R964,D273,R265,D3,L714,D224,L177,U194,L573,U511,L795,U299,L311,U923,R815,U594,L654,U326,L547,U547,R467,D937,L174,U453,R635,D551,L365,U355,R658,U996,R458,D623,R61,U181,R340,U163,L329,D496,L787,D335,L37,D565,R318,U942,R198,U85,R328,D826,R817,D118,R138,D29,L434,D427,R222,D866,L10,D152,R822,D779,L900,D307,R723,D363,L715,D60,R661,U680,R782,U789,R311,D36,R425,U498,L910,D546,R394,D52,R803,D168,L6,U769,R856,D999,L786,U695,R568,U236,R472,U291,L530,U314,L251,D598,R648,D475,L132,D236,L915,D695,L700,U378,L685,D240,R924,D977,R627,U824,L165")
assert(intersect_distance(lines_a, lines_b) == 529)

wire1 = Wire("R75,D30,R83,U83,L12,D49,R71,U7,L72")
wire2 = Wire("U62,R66,U55,R34,D71,R55,D58,R83")
assert_equals(minimal_signal_delay(wire1, wire2), 610)

# part 2
assert_equals(minimal_signal_delay(lines_a, lines_b), "unknown")
