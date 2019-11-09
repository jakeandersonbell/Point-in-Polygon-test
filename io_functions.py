"""This class holds all input functions"""

from geometry_class import *
import os


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
    digits = "1234567890 ."
    while inp.lower() != 'q':  #
        inp = input("Please enter a space-separated coordinate pair: ")
        if inp != 'q':
            for i in inp:
                if i not in digits:
                    inp = inp.replace(i, '')
            if len(inp.split()) != 2:
                print("You did not enter a correctly formatted coordinate pair!\nTry again...\n")
            else:
                points.append(inp.split())
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
    shapes = [points, polygon]  # Both shapes are loaded in so the user can do multiple transformations
    loop = input("Shape loading complete!\n\nWould you like to perform any transformations on your geometries?: "
                 "[Y]/n\n")
    unexpected_inp = "Sorry, that was an unexpected input, please try again...\n\n"
    while loop == "" or loop.lower() == "y" or loop.lower() == "yes":
        loop2 = True
        while loop2:  # Geometry option loop
            shape_choice = input("Which geometry would you like to transform?\n\n[1] Point\n\n[2] Polygon\n\n")
            if shape_choice == '1' or shape_choice == '2':
                loop2 = False
                shape_choice = int(shape_choice) - 1
            else:
                print(unexpected_inp)
        loop3 = True
        while loop3:  # Transformation option loop
            inp = int(input("What translation would you like to perform\n\n[1] Scale\n\n[2] Invert\n\n[3] Rotate\n\n"))
            if inp == 1 or inp == 2 or inp == 3:
                loop3 = False
            else:
                print(unexpected_inp)
        if inp == 1:
            loop4 = True
            while loop4:  # Scaling loop
                try:
                    inp = float(input("By what factor would you like to scale the geometry?: "))
                except ValueError:
                    print(unexpected_inp)
                if isinstance(inp, float):
                    loop4 = False
            shapes[shape_choice].scale(inp)
            print("Geometry scaling complete!")
        elif inp == 2:
            shapes[shape_choice].invert()
            print("Geometry inversion complete!")
        elif inp == 3:
            digits = "1234567890 "  # These are the only characters we want
            loop5 = True
            while loop5:  # Rotation origin option loop
                inp = input("As a space separated coordinate pair, please enter the origin around which you wish to"
                            "rotate the geometry: ")
                for i in inp:
                    if i not in digits:
                        inp = inp.replace(i, '')
                if len(inp.split()) != 2:
                    print("You did not enter a correctly formatted coordinate pair!\nTry again...\n")
                else:
                    origin = inp.split()
                    loop5 = False
            loop6 = True
            while loop6:  # Rotation angle loop
                try:
                    degrees = float(input("By how many degrees would you like to rotate the geometry?: "))
                except ValueError:
                    print(unexpected_inp)
                else:
                    loop6 = False
                    shapes[shape_choice].rotate(degrees, [float(origin[0]), float(origin[1])])
            print("Geometry rotation complete!")

        loop = input("Would you like to do an other transformation?: [Y]/n")

    shapes[0] = shapes[0].make_points()
    shapes[1] = shapes[1].make_poly(polygon.get_name())
    return shapes


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
        if len(files) == 2:
            if os.path.exists(files[0]) and os.path.exists(files[1]):
                polygon_file = files[0]
                points_file = files[1]
            else:
                polygon_file, points_file = 'polygon.csv', 'input.csv'
        else:
            polygon_file, points_file = 'polygon.csv', 'input.csv'
    except NameError:  # if files variable has not been defined
        polygon_file, points_file = 'polygon.csv', 'input.csv'
    return [polygon_file, points_file]
