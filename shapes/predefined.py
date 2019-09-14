import math

from point import Point
import point_array

def generate_box():
    """ Generates a predetermined zigzag line that can be used to test
    the response to sharp corners"""
    points = []
    points.extend(point_array.generate_line_segment(Point(0, 0), Point(0, 5), 20))
    points.extend(point_array.generate_line_segment(Point(0, 5), Point(5, 5), 20))
    points.extend(point_array.generate_line_segment(Point(5, 5), Point(5, 0), 20))
    return points


def generate_step():
    """ Generates a single step to make it easy to check overshoot """
    points = []
    points.extend(point_array.generate_line_segment(Point(0, 0), Point(5, 0), 20))
    points.extend(point_array.generate_line_segment(Point(5, 5), Point(10, 5), 20))
    return points


def generate_sine():
    """ Generates a predetermined zigzag line that can be used to test
    corner-cutting on a more natural shape """
    points = []
    for x in range(100):
        points.append(Point(x/20, math.sin(x/20)*2.5 + 2.5))
    return points
    
