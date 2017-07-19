import numpy as np




def interpolate(z1, z2, z3, z4, x):
    """
    Third Order Interpolation function
    Reference: Section 2.5.7.1 of GSA's "Ionospheric Correction
    Algorithm for Galileo Single Frequency Users"

    :param z1:
    :param z2:
    :param z3:
    :param z4:
    :param x:
    :return:
    """
    if abs(2 * x) < 10 ** -10:
        return z2

    delta = 2 * x - 1
    g1 = z3 + z2
    g2 = z3 - z2
    g3 = z4 + z1
    g4 = (z4 - z1) / 3.0

    a0 = 9 * g1 - g3
    a1 = 9 * g2 - g4
    a2 = g3 - g1
    a3 = g4 - g2

    return 1 / 16.0 * (a0 + a1 * delta + a2 * delta ** 2 + a3 * delta ** 3)


def epstein(peak_amp, peak_height, thickness, H):
    return peak_amp * NeqClipExp((H - peak_height) / thickness) / np.power((1 + NeqClipExp((H - peak_height) / thickness)), 2)


def NeqJoin(dF1, dF2, dAlpha, dX):
    """
    Allows smooth joining of functions f1 and f2 (i.e. continuous first derivatives) at origin.
    Alpha determines width of transition region. Calculates value of joined functions at x.
    :param dF1:
    :param dF2:
    :param dAlpha:
    :param dX:
    :return:
    """
    ee = NeqClipExp(dAlpha * dX)
    return (dF1 * ee + dF2) / (ee + 1)


def NeqClipExp(dPower):
    """

    :param dPower: Power for exponential function [double]
    :return:
    """
    mask1 = np.logical_and(dPower < 80, dPower < 80)
    mask2 = dPower > 80
    mask3 = dPower < -80
    out = np.exp(dPower, where=mask1)
    if type(out) == np.ndarray:
        out[mask2] = 5.5406 * 10 ** 34
        out[mask3]= 1.8049 * 10 ** -35
    else:
        if mask2:
            out = 5.5406 * 10 ** 34
        elif mask3:
            out = 1.8049 * 10 ** -35

    assert( not np.any(out < 0))
    return out


def NeqCriticalFreqToNe(f0):
    """

    :param f0: peak plasma frequency of layer [MHz]
    :return:
    """
    return 0.124 * f0 ** 2
