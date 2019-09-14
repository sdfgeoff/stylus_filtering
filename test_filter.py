from filters import *

def test_fir_filter():
    f = fir_filter([0.5, 0.2, 0.3])
    assert f(Point(0, 0)) == Point(0.0, 0.0)
    assert f(Point(0, 0)) == Point(0.0, 0.0)
    assert f(Point(0, 0)) == Point(0.0, 0.0)
    assert f(Point(0, 0)) == Point(0.0, 0.0)
    assert f(Point(1, 0)) == Point(0.5, 0.0)
    assert f(Point(0, 1)) == Point(0.2, 0.5)
    assert f(Point(0, 1)) == Point(0.3, 0.7)
    assert f(Point(0, 0)) == Point(0.0, 0.5)
    assert f(Point(0, 0)) == Point(0.0, 0.3)
    assert f(Point(0, 0)) == Point(0.0, 0.0)


def test_fir_filter_zero_start():
    f = fir_filter([0.5, 0.2, 0.3])
    assert f(Point(1, 0)) == Point(1.0, 0.0)


def test_mean_filter():
    f = mean_filter(4)
    assert f(Point(0, 0)) == Point(0.0, 0.0)
    assert f(Point(0, 0)) == Point(0.0, 0.0)
    assert f(Point(0, 0)) == Point(0.0, 0.0)
    assert f(Point(0, 0)) == Point(0.0, 0.0)
    assert f(Point(1, 0)) == Point(0.25, 0.0)
    assert f(Point(0, 1)) == Point(0.25, 0.25)
    assert f(Point(0, 1)) == Point(0.25, 0.5)
    assert f(Point(0, 0)) == Point(0.25, 0.5)
    assert f(Point(0, 0)) == Point(0.0, 0.5)
    assert f(Point(0, 0)) == Point(0.0, 0.25)
    assert f(Point(0, 0)) == Point(0.0, 0.0)


def test_exp_filter():
    f = exp_filter(0.75)
    assert f(Point(1, 0)) == Point(1.0, 0.0)
    assert f(Point(0, 0)) == Point(0.75, 0.0)
    assert f(Point(0, 1)) == Point(0.5625, 0.25)
    assert f(Point(0, 1)) == Point(0.421875, 0.4375)
