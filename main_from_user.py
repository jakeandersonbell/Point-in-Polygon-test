import geometry_class as geo
import plotter as plt
import tests as test
import io_functions as io

# Read csv
pl1 = io.read_csv('polygon.csv', 'polygon', 'Poly1')
ps1 = io.user_input('points')

# Tests
test.in_bb(ps1, pl1)
test.on_line([p for p in ps1 if p.get_state() == 'in_bb'], pl1)
test.ray_caster([p for p in ps1 if p.get_state() != 'boundary' and p.get_state() == 'in_bb'], pl1)
test.set_rem_state(ps1)

# Write the result of each point in a csv file
io.write_csv(ps1, 'output.csv', state=True)

# Plotting
boundary_points = [p for p in ps1 if p.get_state() == 'boundary']
inside_points = [p for p in ps1 if p.get_state() == 'inside']
outside_points = [p for p in ps1 if p.get_state() == 'outside']

plot = plt.Plotter()
plot.add_polygon(pl1.all_x(), pl1.all_y())
plot.add_point([p.get_x() for p in boundary_points], [p.get_y() for p in boundary_points], 'boundary')
plot.add_point([p.get_x() for p in inside_points], [p.get_y() for p in inside_points], 'inside')
plot.add_point([p.get_x() for p in outside_points], [p.get_y() for p in outside_points], 'outside')
plot.show()