from point import Point, add_points, invert_point, scale_point, squared_dist_points

def point_array_to_axis_arrays(points):
	""" Separates an array of points into two arrays: one of all the X
	values and one of all the Y values. This is useful for plotting """
	return (
		tuple(p.x for p in points),
		tuple(p.y for p in points)
	)


def sum_point_arrays(pa1, pa2):
	""" Adds the matching points inside two point arrays to create
	one array of the same length of the input arrays. Input arrays
	must be the same length"""
	assert len(pa1) == len(pa2)
	out_array = tuple(add_points(p1, p2) for p1, p2 in zip(pa1, pa2))
	return out_array


def generate_line_segment(start_point, end_point, steps):
	""" Returns an array of points starting at start point, ending at
	end_point, with the defined number of steps. Note that 
	end point is NOT included, so that consecutive line segments
	cane be joined easily."""
	points = []
	
	total_delta = add_points(invert_point(start_point), end_point)
	for i in range(steps):
		percent = i / steps
		current_delta = scale_point(total_delta, percent)
		current_point = add_points(start_point, current_delta)
		points.append(current_point)
	return points


def squared_difference(point_array_1, point_array_2):
    """ Returns the sum of squared error between two point arrays """
    assert len(point_array_1) == len(point_array_2)
    squared_delta = 0
    for p_id, p1 in enumerate(point_array_1):
        p2 = point_array_2[p_id]
        squared_delta += squared_dist_points(p1, p2)
    return squared_delta / len(point_array_1)
