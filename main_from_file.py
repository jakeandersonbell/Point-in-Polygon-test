import geometry_class as geo
import plotter as plt
import tests as test

# Read csv
pl1 = geo.read_csv('polygon.csv', 'polygon', 'Poly1')

ps1 = geo.read_csv('input.csv', 'points')

# Tests
test.in_bb(ps1, pl1)

test.on_line([p for p in ps1 if p.get_state() == "in_bb"], pl1)

test.ray_caster([p for p in ps1 if not p.get_state() == "boundary"], pl1)

# Plotting
boundary_points = [p for p in ps1 if p.get_state() == "boundary"]
inside_points = [p for p in ps1 if p.get_state() == "inside"]
outside_points = [p for p in ps1 if p.get_state() == "boundary"]


plot = plt.Plotter()
plot.add_polygon(pl1.all_x(), pl1.all_y())
plot.add_point([p.get_x() for p in boundary_points], [p.get_y() for p in boundary_points], "boundary")
plot.add_point([p.get_x() for p in inside_points], [p.get_y() for p in inside_points], "inside")
plot.show()

# Write the result of each point in a csv file
#   With open csv w as file
#       for result in results
#           writelines point.get_name() + result
#

# Plot the points and polygon in a plot window
#   plt.plot points/polygon
