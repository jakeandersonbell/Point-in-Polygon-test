import geometry_class as geo
import matplotlib.pyplot as plt
import test_old as test
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
    ps1 = geo.Polygon("Name", [list(map(float, row[1:3])) for row in data])

pl1.invert()
ps1.invert()
ps1 = ps1.make_points()


test.in_bb(ps1, pl1)

test.on_line([p for p in ps1 if p.get_bb_rel()], pl1)

test.ray_caster([p for p in ps1 if not p.get_state() == "Boundary"], pl1)


# plt.fill(pl1.all_x(), pl1.all_y())
# plt.plot([p.get_x() for p in ps1], [p.get_y() for p in ps1], 'r+')
# for i, txt in enumerate(p.get_state() for p in ps1):  # plot number of intersections on points
#     plt.annotate(txt, ([p.get_x() for p in ps1][i], [p.get_y() for p in ps1][i]))
# plt.show()



# Write the result of each point in a csv file
#   With open csv w as file
#       for result in results
#           writelines point.get_name() + result
#

# Plot the points and polygon in a plot window
#   plt.plot points/polygon
