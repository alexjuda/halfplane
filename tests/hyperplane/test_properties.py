from hypothesis import given, strategies as st
import numpy as np

from halfplane import flat


@st.composite
def _pts(draw, coords=st.floats()) -> flat.Pt:
    x = draw(coords)
    y = draw(coords)
    return flat.Pt(x=x, y=y)


@st.composite
def _hses(draw, coords=st.floats()):
    p1 = draw(_pts(coords=coords))
    p2 = draw(_pts(coords=coords))
    return flat.Hpc(p1=p1, p2=p2)


@st.composite
def _non_empty_eterms(draw, coords=st.floats()):
    hs_set = draw(
        st.frozensets(
            _hses(coords=coords),
            min_size=1,
        )
    )
    return flat.Eterm(hses=hs_set)


class TestEterm:
    @given(
        eterm=_non_empty_eterms(
            coords=st.floats(
                allow_infinity=False,
                allow_nan=False,
                min_value=-10**10,
                max_value=10**10,
            )
        )
    )
    def test_bbox_contains_vertex_centroid(self, eterm: flat.Eterm):
        try:
            xs = eterm.xs
        except ValueError:
            return

        pts = np.vstack([x.point.position2d.reshape(1, -1) for x in xs])
        centroid_pos = np.mean(pts, axis=0)
        centroid = flat.Pt(x=centroid_pos[0], y=centroid_pos[1])

        assert flat.box_contains_pt(eterm.bbox, centroid)
