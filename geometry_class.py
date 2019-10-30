

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

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y


class Line(Geometry):  # Construct line given 2 points

    def __init__(self, name, p1, p2):
        super().__init__(name)
        self.__p1 = p1
        self.__p2 = p2


class Polygon(Geometry):
    # Initialize object with a list of point pairs as second argument
    # Currently has methods get_points and make points but will just use one of these for final program
    # Will use both for testing and go with the best option
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
        point_a = points[0]
        for point_b in points[1:]:
            lines.append(Line(point_a.get_name() + "-" + point_b.get_name(), point_a, point_b))
            point_a = point_b
        lines.append(Line(point_a.get_name() + "-" + points[0].get_name(), point_a, points[0]))
        return lines


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
