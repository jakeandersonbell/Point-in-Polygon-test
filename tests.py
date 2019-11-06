import geometry_class as geo
import math
import matplotlib.pyplot as plt


# Check if point is inside or on boundary of bounding box rectangle -
def in_bb(points, poly):
    for p in points:
        if min(poly.all_x()) <= p.get_x() <= max(poly.all_x()) and min(poly.all_y()) <= p.get_y() <= max(poly.all_y()):
            p.set_state("in_bb")


# Check if points lie on parallel line
def on_line(points, poly):
    # Loop through lines
    for point in points:  # Loop through points that haven't been checked
        for line in poly.get_lines():
            x1, x2, x3 = line.get_p1().get_x(), line.get_p2().get_x(), point.get_x()
            y1, y2, y3 = line.get_p1().get_y(), line.get_p2().get_y(), point.get_y()
            if (y3-y1) * (x2-x1) - (x3-x1) * (y2-y1) == 0:  # Cross product - points are aligned
                dot_prod = (x3 - x1) * (x2 - x1) + (y3 - y1) * (y2 - y1)
                sqr_len_ab = (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)
                if x1 <= x3 <= x2 or x1 >= x3 >= x2:  # Point is within line range
                    if y3 == y1:  # if point is on line
                        point.set_state("Boundary")
                    elif 0 < dot_prod < sqr_len_ab:  # Method based on code from https://stackoverflow.com/questions/
                        # 328107/how-can-you-determine-a-point-is-between-two-other-points-on-a-line-segment
                        point.set_state("Boundary")
                # elif line.is_parallel()[1]:  # Y parallel
                if y1 <= y3 <= y2 or y1 >= y3 >= y2:  # Point is within line range
                    if x3 == x1:  # if point is on line
                        point.set_state("Boundary")
                    elif 0 < dot_prod < sqr_len_ab:
                        point.set_state("Boundary")


def get_rays(points):
    # Construct rays as a list of all points not classed as being on shape boundary
    return [geo.Line("Ray " + str(points.index(p) + 1), p.get_coords(), [math.inf, p.get_y()]) for p in
            [i for i in points if not i.get_state() == "Boundary"]]


def special_cases(ray, poly, line, next_index, prev_index):
    if ray.get_p1().get_y() == line.get_p1().get_y() and ray.get_p1().get_x() < line.get_p1().get_x():  # inline with vertex
        next_l = poly.get_lines()[next_index]
        prev_l = poly.get_lines()[prev_index]  # Check  second to last vertex as last vertex == first
        if line.is_parallel()[0]:
            if next_l.get_p2().get_y() < ray.get_p1().get_y() < prev_l.get_p1().get_y() or \
                    next_l.get_p2().get_y() > ray.get_p1().get_y() > prev_l.get_p1().get_y():
                ray.increment()
        elif prev_l.get_p1().get_y() < ray.get_p1().get_y() < next_l.get_p1().get_y() or \
                prev_l.get_p1().get_y() > ray.get_p1().get_y() > next_l.get_p1().get_y():
            # if not line.is_parallel()[0]:
            ray.increment()  # Neighbouring vertices of intersected polygon vertex are above and below ray


def ray_caster(points, poly):
    rays = get_rays(points)
    for ray in rays:  # [x1, y1], [x inf, y2]
        for line in poly.get_lines():  # [x3, y3], [x4, y4]
            y1, y3, y4 = ray.get_p1().get_y(), line.get_p1().get_y(), line.get_p2().get_y()  # y coords
            x1, x3, x4 = ray.get_p1().get_x(), line.get_p1().get_x(), line.get_p2().get_x()  # x coords
            if y3 < y1 < y4 or y3 > y1 > y4:  # point within line y range
                try:
                    x = x3 + ((y1-y3) * (x4 - x3))/(y4 - y3)  # line intersection equation
                except ZeroDivisionError:  # Handles the case for when subtraction yields 0
                    x = x3
                if x >= x1:  # ray intersects line
                    ray.increment()
        # All lines except first and last
        for i, line in enumerate(poly.get_lines()[1:-1]):
            special_cases(ray, poly, line, i+2, i)  # Index is +1 due to omitting the 0th index from loop

        special_cases(ray, poly, poly.get_lines()[0], 1, -2)  # First line

        if int(ray.get_count()) % 2 == 1:
            points[rays.index(ray)].set_state("Inside")

    plt.fill(poly.all_x(), poly.all_y())
    plt.plot([p.get_x() for p in points], [p.get_y() for p in points], 'r+')
    for i, txt in enumerate(p.get_count() for p in rays):  # plot number of intersections on points
        plt.annotate(txt, ([p.get_x() for p in points][i], [p.get_y() for p in points][i]))
    plt.show()