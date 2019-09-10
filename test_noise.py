from noise import *


def test_white_noise():
    # Test reproducability
    g1 = white_noise(5, 1)
    g2 = white_noise(5, 1)
    assert g1() == g2()
    assert g1() == g2()
    assert g1() == g2()
    assert g1() == g2()
    
    # Test it isn't always returning the same
    r1 = g1()
    r2 = g1()
    assert r1 != r2
