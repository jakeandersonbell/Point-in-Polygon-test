
"""This class holds all input functions"""

from geometry_class import *


def read_csv(file, geo_type, *name):
    """Creates geometry objects
     directly from a cvs read.
    """
    with open(file, 'r') as file:
        data = [d.strip().split(',') for d in
                file.readlines()[1:]]  # This skips the csv header, creates a stripped list
        # Reads rows into polygon object, map function used to apply float function to each str item in the row list
        shape = MultiGeometry(name, [list(map(float, row[1:3])) for row in data])
    if geo_type.lower() == 'points':
        return shape.make_points()
    elif geo_type.lower() == 'polygon':
        return shape.make_poly(name)

def user_input(geo_type, *name):
    print("In order, please enter each point of the geometry\n\n"
          "This should be entered as space-separated coordinate pairs followed by ENTER\n\n"
          "Hit ENTER again to finish, press 'q' at any time to stop.")
    inp = input("Press ENTER to begin.\n")
    points = []
    while inp.lower() != 'q':
        inp = input("Please enter a space-separated coordinate pair: ")
        if inp != 'q':
            points.append(inp.split())
    shape = MultiGeometry(name, [list(map(float, p)) for p in points])
    if geo_type.lower() == 'points':
        return shape.make_points()
    elif geo_type.lower() == 'polygon':
        return shape.make_poly(name)



def write_csv(shape, filename, state=False):
    """Writes coordinates to csv,
    point.get_state() column is optional.
    """
    with open(filename, 'w') as f:
        if state:
            f.write('id,x,y,state\n')  # Header
            for i, p in enumerate(shape):
                f.write(str(i+1) + ',' + str(p.get_x()) + ',' + str(p.get_y()) + ',' + str(p.get_state()) + '\n')
        else:
            f.write('id,x,y')  # Header
            for i, p in enumerate(shape):
                f.write(str(i+1) + ',' + str(p.get_x()) + ',' + str(p.get_y()) + '\n')