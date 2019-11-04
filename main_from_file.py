import geometry_class as geo
import csv
import matplotlib.pyplot as plt
import math

# Read a list of x, y coordinates from a csv and create a polygon object
#   With open csv as file
#       Make list of points into a polygon object
# Make these methods in geometry???
with open('polygon.csv', 'r') as file:
    data = [d.strip().split(',') for d in file.readlines()[1:]]  # This skips the csv header, creates a stripped list
    pl1 = geo.Polygon("Name", [list(map(float, row[1:3])) for row in data])  # Reads float(rows) into polygon object

# Read a list of x, y coordinates from a csv to create a list of points
#       make list of points into a list of point objects
with open('input.csv', 'r') as file:
    data = [d.strip().split(',') for d in file.readlines()[1:]]  # This skips the csv header
    # Same as before except we are executing the make_points() Polygon method - not the most intuitive???
    ps1 = geo.Polygon("Name", [list(map(float, row[1:3])) for row in data]).make_points()

# Check if point is inside or on boundary of bounding box rectangle -
for point in ps1:
    if min(pl1.all_x()) <= point.get_x() <= max(pl1.all_x()) and min(pl1.all_y()) <= point.get_y() <= max(pl1.all_y()):
        point.set_bb_rel(True)
    else:
        point.set_bb_rel(False)

# Check if points lie on parallel line
for line in pl1.get_lines():  # Loop through lines
    for point in [x for x in ps1 if not x.get_boundary_rel()]:  # Loop through points that haven't been checked as True
        if line.is_parallel()[0]:  # X parallel
            if point.get_x() == line.get_p1().get_x():  # if point is on line
                point.set_boundary_rel(True)
            else:
                point.set_boundary_rel(False)
        elif line.is_parallel()[1]:  # Y parallel
            if point.get_y() == line.get_p1().get_y():  # if point is on line
                point.set_boundary_rel(True)
            else:
                point.set_boundary_rel(False)

rays = [geo.Line("Ray "+str(ps1.index(p)+1), p.get_coords(), [math.inf, p.get_y()]) for p in ps1]

for ray in rays:  # [x1, y1], [x inf, y2]
    for line in pl1.get_lines():  # [x3, y3], [x4, y4]
        y1, y3, y4 = ray.get_p1().get_y(), line.get_p1().get_y(), line.get_p2().get_y()  # y coords
        x1, x3, x4 = ray.get_p1().get_x(), line.get_p1().get_x(), line.get_p1().get_x()  # x coords
        if line.is_parallel()[0]:  # both X parallel
            # if line.get_p1().get_y() == ray.get_p1().get_y():  # ray and line at same y
            #     if line.get_p1().get_x() > ray.get_p1().get_x() > line.get_p2().get_x() or \
            #             line.get_p1().get_x() < ray.get_p1().get_x() < line.get_p2().get_x():  # point is on a line or to the left of one
            #         ray.increment()
            #         pass
            pass
        elif y3 < y1 < y4 or y3 > y1 > y4:  # point within line bounding box
            try:
                x = x3 + (y1 * (x4 - x3))/((y4 - y3) + y3)  # line intersection equation
            except ZeroDivisionError:
                x = x3
            if x > x1:  # ray intersects line
                ray.increment()




    for i, line in enumerate(pl1.get_lines()):
        if ray.get_p1().get_y() == line.get_p1().get_y() and ray.get_p1().get_x() < line.get_p1().get_x():  # inline with vertex
            if pl1.make_points()[i-1].get_y() < ray.get_p1().get_y() > pl1.make_points()[i+1].get_y() or \
                    pl1.make_points()[i-1].get_y() > ray.get_p1().get_y() < pl1.make_points()[i+1].get_y():
                pass
            elif pl1.make_points()[i-1].get_y() < ray.get_p1().get_y() < pl1.make_points()[i+1].get_y() or \
                    pl1.make_points()[i-1].get_y() > ray.get_p1().get_y() > pl1.make_points()[i+1].get_y():
                # if not line.is_parallel()[0]:
                ray.increment()  # Neighbouring vertices of intersected polygon vertex are above and below ray
            elif ray.get_count() % 2 == 1:  # Checks odd counts to see if they are intersecting vertex without entering shape
                if pl1.make_points()[i-1].get_y() < ray.get_p1().get_y():
                    ray.increment()





plt.fill(pl1.all_x(), pl1.all_y())
plt.plot([p.get_x() for p in ps1], [p.get_y() for p in ps1], 'r+')
for i, txt in enumerate(p.get_count() for p in rays):  # plot number of intersections on points
    plt.annotate(txt, ([p.get_x() for p in ps1][i], [p.get_y() for p in ps1][i]))
plt.show()

#       Line crossing - line1 = [x1, y1], [xinf, y2] - line2 = [x3, y3], [x4, y4]
#           if line1.parallel_x and line2.parallel_x:
#               if y1 == y3:  # lines intersect inf
#                   count += 1
#               else:  #  Don't intersect
#           elif y3 < y1 < y4 or y4 < y1 < y3:
#               x = x3 + (y1 * (x4 - x3))/((y4 - y3) + y3)
#               if x >= x1: #  lines cross
#        Point crossing vertices
#           for i in polygon.make_points():
#               if ray intersects:
#                   if ray.get_y() == polygon.make_points()[i].get_y()
#                       if polygon.make_points()[i-1].get_y() < ray.get_y < polygon.make_points()[i+1].get_y():
#                           count once
#                       elif polygon.make_points()[i-1].get_y() > ray.get_y > polygon.make_points()[i+1].get_y():
#                           count once
#           if count % 0:
#               point outside
#           else:
#               inside

# Write the result of each point in a csv file
#   With open csv w as file
#       for result in results
#           writelines point.get_name() + result
#

# Plot the points and polygon in a plot window
#   plt.plot points/polygon
