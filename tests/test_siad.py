from siad import TrendAdjustedExponentialSmoothing


def test_trend_adjusted_exponential_smoothing():
    values = [54, 63, 73, 73, 49, 47]
    alpha = 0.5
    beta = 0.07

    algorithm = TrendAdjustedExponentialSmoothing(values, alpha, beta, True)

    assert algorithm(2) == 72
    assert algorithm(3) == 81.535
