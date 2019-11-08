
"""This is the program for reading csv and user input"""

import sys
import plotter as plt
import tests as test
import io_functions as io

if __name__ == "__main__":

    # Check if file paths have been given as command line arguments
    polygon_file, points_file = io.command_line_args(sys.argv)[0], io.command_line_args(sys.argv)[1]

    # Read csv and user input
    pl1 = io.read_csv(polygon_file, 'polygon', name='Poly1', trans_options=True)
    ps1 = io.user_input('points', trans_options=True)

    # Transformation options allows user to transform geometries
    geometries = io.transform_options(ps1, pl1)
    ps1, pl1 = geometries[0], geometries[1]

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