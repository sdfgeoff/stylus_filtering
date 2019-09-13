import random
from point import Point


def white_noise(seed, magnitude):
	""" Returns a function that, when called, returns a point containing
	white noise with the specified magnitude """
	generator = random.Random(seed)
	def generate():
		return Point(
			generator.gauss(0, magnitude),
			generator.gauss(0, magnitude)
		)
	return generate


def generate_noise_array(generator, length):
	return tuple(generator() for _ in range(length))
