from point import *

def test_add_points():
	assert add_points(Point(1, 1), Point(-3, 3)) == Point(-2, 4)

def test_invert_point():
	assert invert_point(Point(1, -5)) == Point(-1, 5)

def test_scale_point():
	assert scale_point(Point(2, -4), 2) == Point(4, -8)

def test_length_squared_point():
	assert length_squared_point(Point(2, 2)) == 8
	
def test_squared_dist_points():
	assert squared_dist_points(Point(2, 2), Point(4, 4)) == 8

