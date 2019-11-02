import matplotlib.pyplot as plt
import math


class Geometry:  # The base class to hold name and name method

    # Define a class geometry with private name attribute
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name


class Point(Geometry):  # Points class to have methods get_x, get_y

    def __init__(self, name, x, y):
        super().__init__(name)
        self.__x = x
        self.__y = y
        self.__in_bb = False
        self.__on_boundary = False
        self.__count = 0

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_coords(self):
        return [self.__x, self.__y]

    def set_bb_rel(self, state):  # bounding box relationship
        self.__in_bb = state

    def get_bb_rel(self):
        return self.__in_bb

    def set_boundary_rel(self, state):  # boundary relationship
        self.__on_boundary = state

    def get_boundary_rel(self):
        return self.__on_boundary


class Line(Geometry):  # Construct line given a name and 2 points yx lists, then constructs point objects

    def __init__(self, name, p1, p2):
        super().__init__(name)
        self.__p1 = Point(str(name) + ": 1", p1[0], p1[1])
        self.__p2 = Point(str(name) + ": 2", p2[0], p2[1])
        self.__count = 0

    def get_p1(self):
        return self.__p1

    def get_p2(self):
        return self.__p2

    def is_parallel(self):  # Returns
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


class Polygon(Geometry):
    # Initialize object with a list of point pairs as second argument
    # Currently has methods get_points and make points but will just use one of these for final program
    # Will use both for testing and go with the best option
    # Convert all points to float on construction
    def __init__(self, name, points):
        super().__init__(name)
        self.__points = points

    def get_points(self):  # Return a list fo coordinate lists
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
        return [i[0] for i in self.get_points()]

    def all_y(self):
        return [i[1] for i in self.get_points()]


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
