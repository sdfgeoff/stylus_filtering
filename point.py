from collections import namedtuple

# Create a datatype to represent an immutable point
Point = namedtuple("Point", ["x", "y"])


def add_points(p1, p2):
	""" Return a new point from the sum of two """
	return Point(p1.x + p2.x, p1.y + p2.y)


def invert_point(p1):
	""" Returns the inverse of a point. Use with add_points to do 
	a subtraction """
	return scale_point(p1, -1)


def scale_point(p1, scale):
	""" Scales a point by a factor """
	return Point(p1.x * scale, p1.y * scale)


def length_squared_point(p1):
	""" Returns the squared distance of a point from 0,0 """
	return p1.x ** 2 + p1.y ** 2


def squared_dist_points(p1, p2):
	return length_squared_point(add_points(p1, invert_point(p2)))

