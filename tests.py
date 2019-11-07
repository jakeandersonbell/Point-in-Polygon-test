
"""This file holds all functions for testing point-polygon geometry relationships."""

import geometry_class as geo
import math
import matplotlib.pyplot as plt


def in_bb(points, poly):
    """This function checks if point is inside
    or on boundary of bounding box rectangle
    """
    for p in points:
        if min(poly.all_x()) <= p.get_x() <= max(poly.all_x()) and min(poly.all_y()) <= p.get_y() <= max(poly.all_y()):
            p.set_state('in_bb')


# Check if points lie on parallel line
def on_line(points, poly):
    """This function checks point-on-line
    relationships using the cross-product method.

    Method adapted from code from https://stackoverflow.com/questions/328107/
    how-can-you-determine-a-point-is-between-two-other-points-on-a-line-segment
    """
    for point in points:
        for line in poly.get_lines():
            x1, x2, x3 = line.get_p1().get_x(), line.get_p2().get_x(), point.get_x()
            y1, y2, y3 = line.get_p1().get_y(), line.get_p2().get_y(), point.get_y()
            if (y3-y1) * (x2-x1) - (x3-x1) * (y2-y1) == 0:  # if Cross product ==0: points are aligned
                dot_prod = (x3 - x1) * (x2 - x1) + (y3 - y1) * (y2 - y1)
                sqr_len_ab = (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)
                if x1 <= x3 <= x2 or x1 >= x3 >= x2:  # Point is within line range
                    if y3 == y1 or 0 < dot_prod < sqr_len_ab:  # if point is on line
                        point.set_state('Boundary')
                if y1 <= y3 <= y2 or y1 >= y3 >= y2:  # Point is within line range
                    if x3 == x1 or 0 < dot_prod < sqr_len_ab:  # if point is on line
                        point.set_state('Boundary')


def special_cases(ray, poly, line, next_index, prev_index):
    """This function tests for special
    cases in point-line relationships.
    """
    if ray.get_p1().get_y() == line.get_p1().get_y() and \
            ray.get_p1().get_x() < line.get_p1().get_x():  # Inline and to left of vertex
        next_l = poly.get_lines()[next_index]
        prev_l = poly.get_lines()[prev_index]
        if line.is_parallel()[0]:
            # If parallel check that neighbour+1 nodes are above and below line, will not class an entry otherwise
            if next_l.get_p2().get_y() < ray.get_p1().get_y() < prev_l.get_p1().get_y() or \
                    next_l.get_p2().get_y() > ray.get_p1().get_y() > prev_l.get_p1().get_y():
                ray.increment()
        elif prev_l.get_p1().get_y() < ray.get_p1().get_y() < next_l.get_p1().get_y() or \
                prev_l.get_p1().get_y() > ray.get_p1().get_y() > next_l.get_p1().get_y():
            ray.increment()  # Neighbouring vertices of intersected polygon vertex are above and below ray


def ray_caster(points, poly):
    """This function conducts the ray casting line
    intersection algorithm then runs the special cases.
    """
    # Rays are lines constructed from points that haven't been classed as boundary
    rays = [geo.Line('Ray ' + str(points.index(p) + 1), p.get_coords(), [math.inf, p.get_y()]) for p in
            [i for i in points if not i.get_state() == 'Boundary']]
    for ray in rays:  # [x1, y1], [x inf, y2]
        for line in poly.get_lines():  # [x3, y3], [x4, y4]
            y1, y3, y4 = ray.get_p1().get_y(), line.get_p1().get_y(), line.get_p2().get_y()
            x1, x3, x4 = ray.get_p1().get_x(), line.get_p1().get_x(), line.get_p2().get_x()
            if y3 < y1 < y4 or y3 > y1 > y4:  # point within line y range
                try:
                    x = x3 + ((y1-y3) * (x4 - x3))/(y4 - y3)  # line intersection equation
                except ZeroDivisionError:  # Handles the case for when subtraction yields 0
                    x = x3
                if x >= x1:  # ray intersects line
                    ray.increment()
        # All lines except first and last
        for i, line in enumerate(poly.get_lines()[1:-1]):
            special_cases(ray, poly, line, i+2, i)  # next/prev line index is +1 due to omitting the 0th index from loop

        # First line
        special_cases(ray, poly, poly.get_lines()[0], 1, -2)  # prev_l is second to last vertex as last vertex == first

        if int(ray.get_count()) % 2 == 1:
            points[rays.index(ray)].set_state('Inside')


def set_rem_state(points):
    """Sets state for remaining points.
    """
    for point in [p for p in points if p.get_state() != 'inside' and p.get_state() != 'boundary']:
        point.set_state('outside')
