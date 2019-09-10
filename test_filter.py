from filters import *

def test_fir_filter():
    f = fir_filter([0.5, 0.2, 0.3])
    assert f(Point(1, 0)) == Point(0.5, 0.0)
    assert f(Point(0, 1)) == Point(0.2, 0.5)
    assert f(Point(0, 1)) == Point(0.3, 0.7)
    assert f(Point(0, 0)) == Point(0.0, 0.5)
    assert f(Point(0, 0)) == Point(0.0, 0.3)
    assert f(Point(0, 0)) == Point(0.0, 0.0)

def test_mean_filter():
    f = mean_filter(4)
    assert f(Point(1, 0)) == Point(0.25, 0.0)
    assert f(Point(0, 1)) == Point(0.25, 0.25)
    assert f(Point(0, 1)) == Point(0.25, 0.5)
    assert f(Point(0, 0)) == Point(0.25, 0.5)
    assert f(Point(0, 0)) == Point(0.0, 0.5)
    assert f(Point(0, 0)) == Point(0.0, 0.25)
    assert f(Point(0, 0)) == Point(0.0, 0.0)


def test_exp_filter():
    f = exp_filter(0.75)
    assert f(Point(1, 0)) == Point(0.25, 0.0)
    assert f(Point(0, 1)) == Point(0.1875, 0.25)
    assert f(Point(0, 1)) == Point(0.140625, 0.4375)
    assert f(Point(0, 1)) == Point(0.10546875, 0.578125)
    assert f(Point(0, 1)) == Point(0.0791015625, 0.68359375)
    assert f(Point(0, 1)) == Point(0.059326171875, 0.7626953125)
    assert f(Point(0, 1)) == Point(0.04449462890625, 0.822021484375)
