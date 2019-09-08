from point_array import *

def test_point_array_to_axis_arrays():
	assert point_array_to_axis_arrays([
		Point(0, 0),
		Point(1, 2),
		Point(-1, 4),
	]) == ((0, 1, -1), (0, 2, 4))


def test_sum_point_arrays():
	assert sum_point_arrays(
		[Point(0, 0), Point(1, 1), Point(2, 2)],
		[Point(1, 1), Point(-2, 2), Point(1, 1)]
	) == (Point(1, 1), Point(-1, 3), Point(3, 3))


def test_generate_line():
	assert generate_line_segment(Point(1, 1), Point(6, 6), 5) == [
		Point(1, 1),
		Point(2, 2),
		Point(3, 3),
		Point(4, 4),
		Point(5, 5),
	]
