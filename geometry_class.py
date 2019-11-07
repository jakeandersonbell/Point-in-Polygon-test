
"""This file holds all classes and methods for geometry objects."""


class Geometry:
    """Defines the base class to hold name,
    all objects hereafter inherit name.
    """
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name


class MultiGeometry(Geometry):
    """Defines the base multi-geometry class, holds
    methods for dealing with multi-point data and allows
    for the conversion of Multi-geo into other objects.
    """
    def __init__(self, name, points):
        super().__init__(name)
        self.__name = name
        self.__points = points

    def make_points(self):  # Returns a list of point objects
        # Converts points list of coordinates to a list of Point objects, name increments with index +1
        return [Point('Point ' + str(self.__points.index(i) + 1), i[0], i[1]) for i in self.__points]

    def make_poly(self, name):  # Returns a Polygon object
        return Polygon(name, self.__points)

    def invert(self):  # Returns inverted coordinates
        return [[c * -1 for c in p] for p in self.__points]  # c = coordinate, p = point

    def scale(self, factor):  # Returns coordinates scaled by a given factor
        return [[c * factor for c in p] for p in self.__points]  # c = coordinate, p = point


class Point(Geometry):
    """Initialised by a name, then x and y
    value as separate parameters.
    """
    def __init__(self, name, x, y):
        super().__init__(name)
        self.__name = name
        self.__x = x
        self.__y = y
        self.__count = 0
        self.__state = False

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_coords(self):  # Return a coordinate pair list
        return [self.__x, self.__y]

    def set_state(self, state):
        # This method is used for applying the point-polygon relationship after checking
        self.__state = state.lower()

    def get_state(self):
        return self.__state


class Line(Geometry):
    """Initialised by a name, then
    2 comma-separated x, y lists.
    """
    def __init__(self, name, p1, p2):
        super().__init__(name)
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
        if self.__p1.get_x() == self.__p2.get_x():
            parallel_y = True
        else:
            parallel_y = False
        return [parallel_x, parallel_y]

    def increment(self):  # Used for counting the number of intersections
        self.__count += 1

    def get_count(self):
        return self.__count


class Polygon(MultiGeometry):
    """Initialize object with name, then a list
    of point coordinate pairs as second argument.
    """
    def __init__(self, name, points):
        super().__init__(name, points)
        self.__name = name
        self.__points = points

    def invert(self):  # See MultiGeometry
        return Polygon(self.__name, super().invert())

    def scale(self, factor):  # See MultiGeometry
        return Polygon(self.__name, super().scale(factor))

    def get_coords(self):  # Return a list of coordinate pair lists
        return self.__points

    def get_lines(self):  # Return a list of Line objects
        points = super().make_points()
        lines = []
        pnt_a = points[0]
        for pnt_b in points[1:]:
            lines.append(Line(pnt_a.get_name() + "-" + pnt_b.get_name(), pnt_a.get_coords(), pnt_b.get_coords()))
            pnt_a = pnt_b
        lines.append(Line(pnt_a.get_name() + "-" + points[0].get_name(), pnt_a.get_coords(), points[0].get_coords()))
        return lines

    def all_x(self):  # Returns a list of x values
        return [i[0] for i in self.get_coords()]

    def all_y(self):  # Returns a list of y values
        return [i[1] for i in self.get_coords()]

    def get_area(self):
        """Returns shape area based in the shoelace algorithm.
        Supports closed and open shapes.
        """
        sum_x = 0.0
        sum_y = 0.0
        last_v = -1
        if super().make_points()[0].get_coords() == super().make_points()[-1].get_coords():
            last_v = -2  # if polygon is closed ignore last point as it is the same as first
        for i in range(len(self.all_x()[:last_v])):  # Shoelace formula
            sum_x += self.all_x()[i] * self.all_y()[i+1]
            sum_y += self.all_x()[i+1] * self.all_y()[i]
        sum_x += self.all_x()[last_v] * self.all_y()[0]
        sum_y += self.all_x()[0] * self.all_y()[last_v]
        return abs(sum_x - sum_y)/2


