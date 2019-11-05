import geometry_class as geo
import math

# Check if point is inside or on boundary of bounding box rectangle -
def in_bb(points, poly):
    for p in points:
        if min(poly.all_x()) <= p.get_x() <= max(poly.all_x()) and min(poly.all_y()) <= p.get_y() <= max(poly.all_y()):
            p.set_bb_rel(True)
        else:
            p.set_bb_rel(False)

# Check if points lie on parallel line
def on_line(points, poly):
      # Loop through lines
    for point in points:  # Loop through points that haven't been checked
        for line in poly.get_lines():
            x1, x2, x3 = line.get_p1().get_x(), line.get_p2().get_x(), point.get_x()
            y1, y2, y3 = line.get_p1().get_y(), line.get_p2().get_y(), point.get_y()
            if (y3-y1) * (x2-x1) - (x3-x1) * (y2-y1) == 0:  # Cross product - points are aligned
                dotprod = (x3 - x1) * (x2 - x1) + (y3 - y1) * (y2 - y1)
                sqrlenab = (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)
                if x1 <= x3 <= x2 or x1 >= x3 >= x2:  # Point is within line range
                    if y3 == y1:  # if point is on line
                        point.set_boundary_rel(True)
                        point.set_state("Boundary")
                    elif 0 < dotprod < sqrlenab:  # Expression based on code from https://stackoverflow.com/questions/
                        # 328107/how-can-you-determine-a-point-is-between-two-other-points-on-a-line-segment
                        point.set_boundary_rel(True)
                        point.set_state("Boundary")
                # elif line.is_parallel()[1]:  # Y parallel
                if y1 <= y3 <= y2 or y1 >= y3 >= y2:  # Point is within line range
                    if x3 == x1:  # if point is on line
                        point.set_boundary_rel(True)
                        point.set_state("Boundary")
                    elif 0 < dotprod < sqrlenab:
                        point.set_boundary_rel(True)
                        point.set_state("Boundary")


def get_rays(points):
    return [geo.Line("Ray " + str(points.index(p) + 1), p.get_coords(), [math.inf, p.get_y()]) for p in points]


def ray_caster(points, poly):
    rays = get_rays(points)
    for ray in rays:  # [x1, y1], [x inf, y2]
        for line in poly.get_lines():  # [x3, y3], [x4, y4]
            y1, y3, y4 = ray.get_p1().get_y(), line.get_p1().get_y(), line.get_p2().get_y()  # y coords
            x1, x3, x4 = ray.get_p1().get_x(), line.get_p1().get_x(), line.get_p1().get_x()  # x coords
            if y3 < y1 < y4 or y3 > y1 > y4:  # point within line bounding box
                try:
                    x = x3 + (y1 * (x4 - x3))/((y4 - y3) + y3)  # line intersection equation
                except ZeroDivisionError:
                    x = x3
                if x > x1:  # ray intersects line
                    ray.increment()
        for i, line in enumerate(poly.get_lines()):
            if ray.get_p1().get_y() == line.get_p1().get_y() and ray.get_p1().get_x() < line.get_p1().get_x():  # inline with vertex
                if poly.make_points()[i - 1].get_y() < ray.get_p1().get_y() < poly.make_points()[i + 1].get_y() or \
                        poly.make_points()[i - 1].get_y() > ray.get_p1().get_y() > poly.make_points()[i + 1].get_y():
                    # if not line.is_parallel()[0]:
                    ray.increment()  # Neighbouring vertices of intersected polygon vertex are above and below ray
                elif ray.get_count() % 2 == 1:  # Checks odd counts to see if the rays are intersecting vertex without
                    # entering shape, if they are increment
                    if poly.make_points()[i-1].get_y() < ray.get_p1().get_y() and poly.get_lines()[i].is_parallel()[0]:
                        ray.increment()
                    elif poly.make_points()[i - 1].get_y() > ray.get_p1().get_y() and poly.get_lines()[i].is_parallel()[
                        0]:
                        ray.increment()
        if ray.get_count() % 2 == 1:
            points[rays.index(ray)].set_state("inside")