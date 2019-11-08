"""This class holds all input functions"""

from geometry_class import *


def read_csv(file, geo_type, name='Polygon 1', trans_options=False):
    """Creates multi-geometry
    objects from a cvs read.
    """
    with open(file, 'r') as file:
        data = [d.strip().split(',') for d in
                file.readlines()[1:]]  # This skips the csv header, creates a stripped list
        # Reads rows into polygon object, map function used to apply float function to each str item in the row list
        shape = MultiGeometry(name, [list(map(float, row[1:3])) for row in data])
    if not trans_options:
        if geo_type.lower() == 'points':
            return shape.make_points()
        elif geo_type.lower() == 'polygon':
            return shape.make_poly(name)
    else:
        return shape


def user_input(geo_type, *name, trans_options=False):
    """Creates multi-geometry
    objects from user input.
    """
    print("In order, please enter each point of the geometry\n\n"
          "This should be entered as space-separated coordinate pairs followed by ENTER\n\n"
          "Press 'q' at any time to finish.\n")
    inp = input("Press ENTER to begin.\n")
    points = []
    while inp.lower() != 'q':  #
        inp = input("Please enter a space-separated coordinate pair: ")
        if inp != 'q':
            points.append(coord_format(inp))
    shape = MultiGeometry(name, [list(map(float, p)) for p in points])
    if not trans_options:
        if geo_type.lower() == 'points':
            return shape.make_points()
        elif geo_type.lower() == 'polygon':
            return shape.make_poly(name)
    else:
        return shape


def transform_options(points, polygon):
    """This function prompt the user with
    options for geometry transformation.
    """
    shapes = [points, polygon]
    loop = input("Shape loading complete!\n\nWould you like to perform any transformations on your geometries?: "
                 "[Y]/n\n")
    while loop == "" or loop.lower() == "y" or loop.lower() == "yes":
        shape_choice = int(input("Which geometry would you like to transform?\n\n[1] Point\n\n[2] Polygon\n\n")) - 1
        shape = shapes[shape_choice]
        inp = int(input("What translation would you like to perform\n\n[1] Scale\n\n[2] Invert\n\n[3] Rotate\n\n"))
        if inp == 1:
            shape = shape.scale(float(input("By what factor would you like to scale the geometry?: ")))
            print("Geometry scaling complete!")
        elif inp == 2:
            shape = shape.invert()
            print("Geometry inversion complete!")
        elif inp == 3:
            inp = input("As a space separated coordinate pair, please enter the origin around which you wish to"
                        "rotate the geometry: ")
            digits = "1234567890 "  # These are the only characters we want
            while 'origin' not in locals():
                for i in inp:
                    if i not in digits:
                        inp = inp.replace(i, '')
                if len(inp.split()) != 2:
                    print("You did not enter a correctly formatted coordinate pair!\nTry again...\n")
                else:
                    origin = inp.split()
                    break
            shape = shape.rotate(float(input("By how many degrees would you like to rotate the geometry?: ")
                                                  ), [float(origin[0]), float(origin[1])])
            print("Geometry rotation complete!")
        # if shape_choice == 0:
        #     print(shape_choice)
        #     shapes[0] = shape.make_points()
        #     shapes[1] = polygon.make_poly(polygon.get_name())
        # elif shape_choice == 1:
        #     shapes[0] = points.make_points()
        #     shapes[1] = shape.make_poly(shape.get_name())
        loop = input("Would you like to do an other transformation?: [Y]/n")

    shapes[0] = points.make_points()
    shapes[1] = polygon.make_poly(polygon.get_name())
    return shapes


def coord_format(inp):
    digits = "1234567890 "  # These are th only characters we want
    for i in inp:
        if i not in digits:
            inp = inp.replace(i, '')
    if len(inp.split()) != 2:
        print("You did not enter a correctly formatted coordinate pair!\nTry again...\n")
    else:
        return inp.split()


def write_csv(shape, filename, state=False):
    """Writes coordinates to csv,
    point.get_state() column is optional.
    """
    with open(filename, 'w') as f:
        if state:
            f.write('id,x,y,state\n')  # Header
            for i, p in enumerate(shape):
                f.write(str(i + 1) + ',' + str(p.get_x()) + ',' + str(p.get_y()) + ',' + str(p.get_state()) + '\n')
        else:
            f.write('id,x,y')  # Header
            for i, p in enumerate(shape):
                f.write(str(i + 1) + ',' + str(p.get_x()) + ',' + str(p.get_y()) + '\n')


def command_line_args(args):  # 2 file paths must be entered or none at all
    """Function allows user to input file path
    arguments when running program from command line.
    """
    if len(args) > 1:
        files = []
        for arg in [a.lower() for a in args[1:]]:
            if 'csv' in arg:
                files.append(arg)
    try:
        polygon_file = files[0]
        points_file = files[1]
    except NameError:  # if files variable has not been defined
        polygon_file = 'polygon.csv'
        points_file = 'input.csv'
    return [polygon_file, points_file]
