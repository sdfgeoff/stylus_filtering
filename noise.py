""" We want to test how the filters perform with noise. This is where
the noise is generated. Ideally there would be a few different
types of noise.

Noise generators should be seedable and deterministic. Ideally they
should also be controllable (eg in magnitude of noise).
"""
import random
from point import Point


def white_noise(seed, length):
    """ Returns a function that, when called, returns a point containing
    white noise with the specified seed and legnth """
    generator = random.Random(seed)
    def generate():
        return Point(
            (generator.random() - 0.5) * 2.0 * length,
            (generator.random() - 0.5) * 2.0 * length
        )
    return generate


def generate_noise_array(generator, length):
    """ Generates a whole bunch of noise with the given generator """
    return tuple(generator() for _ in range(length))
