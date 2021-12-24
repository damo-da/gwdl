import numpy as np
from sklearn.preprocessing import FunctionTransformer


def _np_array(X):
    """Convert TimeSeries data to a 3-d numpy array."""
    data = []
    for (h1, l1) in X:
        data.append(
            [
                list(h1.data),
                list(l1.data),
            ]
        )

    return np.array(data)


def _signal_filter(X):
    newX = []

    for i, (h1s, l1s) in enumerate(X):
        h1s = h1s.whiten().bandpass(30, 400)
        l1s = l1s.whiten().bandpass(30, 400)

        newX.append([h1s, l1s])

    return newX


class GetWindow:
    """Extract windows from TimeSeries data.

    Each row in the (X) must be of the format
    [h1_strain, l1_strain].
    """

    def __init__(self, window_start, window_end):
        self.ws, self.we = window_start, window_end

    def fit(self, X, y):
        return self

    def transform(self, X):
        return [
            (
                h1.crop(h1.t0.value + self.ws, h1.t0.value + self.we),
                l1.crop(l1.t0.value + self.ws, l1.t0.value + self.we),
            )
            for (h1, l1) in X
        ]


Combine = FunctionTransformer(lambda X: X.reshape(len(X), -1))

NpArrayTransform = FunctionTransformer(_np_array)

SignalFilter = FunctionTransformer(_signal_filter)
