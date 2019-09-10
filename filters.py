from point import Point, add_points, scale_point, invert_point

def null_filter():
	"""Filter which returns points as-is"""
	def process(new_data):
		return new_data
	return process


def fir_filter(weights):
	"""Returns a FIR filter with the specified weights.
	Ie if you pass in the weights [0.3, 0.5, 0.2], and pass in an 
	inpulse ([1, 0, 0]), you will get out the weights as a result"""
	history = []
	def process(new_data):
		nonlocal history
		history.append(new_data)
		
		if len(history) > len(weights):
			history = history[-len(weights):]
		
		p_sum = Point(0, 0)
		for point, weight in zip(reversed(history), weights):
			p_sum = add_points(p_sum, scale_point(point, weight))
			
		return p_sum

	return process
	


def mean_filter(size):
	"""FIR filter with equal weights"""
	return fir_filter([1/size]*size)
	
	
def exp_filter(percent):
	"""IIR filter with the specified decay"""
	prev = None
	
	def process(new_data):
		nonlocal prev
		
		if prev is None:
			prev = new_data
		
		new_point = add_points(
			scale_point(prev, percent),
			scale_point(new_data, 1.0 - percent)
		)
		prev = new_point
		
		return new_point
		
	return process 


def simple_predictive_filter(prediction_factor, velocity_smoothing_factor):
	prev_prediction = None
	est_velocity = Point(0, 0)
	
	def process(new_data):
		nonlocal prev_prediction
		nonlocal est_velocity
		
		if prev_prediction is None:
			prev_prediction = new_data

		current_velocity = add_points(new_data, invert_point(prev_prediction))
		est_velocity = add_points(
			scale_point(est_velocity, velocity_smoothing_factor),
			scale_point(current_velocity, 1.0 - velocity_smoothing_factor)
		)

		predicted_point = add_points(prev_prediction, est_velocity)
		
		smoothed_predicted_point = add_points(
			scale_point(predicted_point, prediction_factor),
			scale_point(prev_prediction, 1.0 - prediction_factor)
		)
		prev_prediction = smoothed_predicted_point
		
		return smoothed_predicted_point
		
	return process 


def filter_array(fltr, points):
	return tuple(fltr(p) for p in points)
	
