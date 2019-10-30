# Import classes
import geometry_class as geo

# Read a list of x, y coordinates from a csv and create a polygon object
#   With open csv as file
#       Make list of points into a polygon object

# Read a list of x, y coordinates from a csv to create a list of points
#   With open csv r as file
#       make list of points into a list of point objects

# Categorises point as being inside, outside or boundary
#   Check minimum bounding rectangle
#       if min_x < point.get_x() < max_x and min_y < point.get_y() < max_y:
#           point in bb
#       else:
#           point can't be inside polygon
#   Ray casting - General rule
#       init line class from point to math.inf along x
#           for line in polygon:
#               if ray intersects line:
#                   count += 1
# Look to move the following to its own .py
#   Ray casting checks
#       Point on line - line = [x1, y1], [x2, y2] - point = x3, y3
#           if x1 == x2:
#               line.parallel_x = True
#               if x1 == x3:  # Point on line
#           elif y1 == y2:
#               parallel_y == True
#               if x1 == y3:  # Point on line
#           elif ((x3-x1)/(x2-x1))*(y2-y1)+y == y3: # Point on line
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
