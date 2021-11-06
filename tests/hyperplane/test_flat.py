import numpy as np
import numpy.testing
from hypothesis import given
from hypothesis.extra.numpy import arrays

from hyperplane import flat


class TestAffineTransform:
    @given(
        vector=arrays(dtype=int, shape=2),
        A1=arrays(dtype=int, shape=(2, 2), unique=True),
        b1=arrays(dtype=int, shape=2),
        A2=arrays(dtype=int, shape=(2, 2), unique=True),
        b2=arrays(dtype=int, shape=2),
    )
    def test_compose_same_as_chained_applies(self, vector, A1, b1, A2, b2):
        af1 = flat.AffineTransform(A1, b1)
        af2 = flat.AffineTransform(A2, b2)

        composed = af2.compose(af1)

        result = composed.apply(vector)
        np.testing.assert_array_equal(result, af2.apply(af1.apply(vector)))
