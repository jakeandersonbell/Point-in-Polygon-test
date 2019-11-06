import math


def read_csv(file, geo_type, *name):  # Allows the creation of geo objects directly from a cvs read
    with open(file, 'r') as file:
        data = [d.strip().split(',') for d in
                file.readlines()[1:]]  # This skips the csv header, creates a stripped list
        shape = Geometry(name, [list(map(float, row[1:3])) for row in data])  # Reads float(rows) into polygon object
    if geo_type.lower() == "points":
        return shape.make_points()
    elif geo_type.lower() == "polygon":
        return shape.make_poly()


class Geometry:  # The base class to hold name and name method

    # Define a class geometry with private name attribute
    def __init__(self, name, points):
        self.__name = name
        self.__points = points

    def get_name(self):
        return self.__name

    def make_points(self):  # Returns a list of point objects
        # Converts points list of coordinates to a list of Point objects, name increments with index +1
        return [Point("Point " + str(self.__points.index(i) + 1), i[0], i[1]) for i in self.__points]

    def make_poly(self):
        return Polygon(self.__name, self.__points)


class Point:  # Points class to have methods get_x, get_y

    def __init__(self, name, x, y):
        self.__name = name
        self.__x = x
        self.__y = y
        self.__count = 0
        self.__state = False

    def get_name(self):
        return self.__name

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_coords(self):  # This method is useful for when converting between geometry objects
        return [self.__x, self.__y]

    def set_state(self, state):
        valid_states = ["Boundary", "Inside", "Outside", "in_bb"]
        if state in valid_states or [v.lower() for v in valid_states]:
            self.__state = state.lower()
        else:
            print("Invalid point state given")

    def get_state(self):
        return self.__state


class Line:  # Construct line given a name and 2 points yx lists, then constructs point objects

    def __init__(self, name, p1, p2):
        self.__name = name
        self.__p1 = Point(str(name) + ": 1", p1[0], p1[1])
        self.__p2 = Point(str(name) + ": 2", p2[0], p2[1])
        self.__count = 0

    def get_p1(self):
        return self.__p1

    def get_p2(self):
        return self.__p2

    def is_parallel(self):  # Returns a list of booleans for parallel state of each dimension
        if self.__p1.get_y() == self.__p2.get_y():
            parallel_x = True
        else:
            parallel_x = False
        if self.__p1.get_x() != math.inf:
            if self.__p1.get_x() == self.__p2.get_x():
                parallel_y = True
            else:
                parallel_y = False
        return [parallel_x, parallel_y]

    def increment(self):
        self.__count += 1

    def get_count(self):
        return self.__count


class Polygon:
    # Initialize object with a list of point pairs as second argument
    def __init__(self, name, points):
        self.__name = name
        self.__points = points

    def invert(self):  # Can invert shapes
        self.__points = [[c * -1 for c in p] for p in self.__points]  # c = coordinate, p = point

    def get_coords(self):  # Return a list fo coordinate pair lists
        return self.__points

    def make_points(self):  # Returns a list of point objects
        # Converts points list of coordinates to a list of Point objects, name increments with index +1
        return [Point("Point " + str(self.__points.index(i) + 1), i[0], i[1]) for i in self.__points]

    def get_lines(self):  # Return a list of Line objects
        points = self.make_points()
        lines = []
        pnt_a = points[0]
        for pnt_b in points[1:]:
            lines.append(Line(pnt_a.get_name() + "-" + pnt_b.get_name(), pnt_a.get_coords(), pnt_b.get_coords()))
            pnt_a = pnt_b
        lines.append(Line(pnt_a.get_name() + "-" + points[0].get_name(), pnt_a.get_coords(), points[0].get_coords()))
        return lines

    def all_x(self):
        return [i[0] for i in self.get_coords()]

    def all_y(self):
        return [i[1] for i in self.get_coords()]


class Triangle(Polygon):
    def __init__(self, name, p1, p2, p3):
        super().__init__(name, [p1, p2, p3])

    def get_area(self):  # Uses the shoelace formula in order to return area
        points = self.make_points()
        res = points[1].get_x() * points[2].get_y() - points[2].get_x() * points[1].get_y()
        res = res - points[0].get_x() * points[2].get_y() + points[2].get_x() * points[0].get_y()
        res = res + points[0].get_x() * points[1].get_y() - points[1].get_x() * points[0].get_y()
        return abs(res) / 2


class Square(Polygon):  # Obtains the 4 point locations from the bottom left point and side in attribute assignment
    def __init__(self, name, bl_point, side):
        bl_point = Point("Bottom left", bl_point[0], bl_point[1])
        points = [bl_point, Point("Top left", bl_point.get_x(), bl_point.get_y() + side),
                  Point("Top right", bl_point.get_x() + side, bl_point.get_y() + side),
                  Point("Bottom right", bl_point.get_x(), bl_point.get_y() + side)]
        super().__init__(name, points)  # Then initialises the points using the parent class
        self.__side = side

    def get_area(self):
        return self.__side ** 2
