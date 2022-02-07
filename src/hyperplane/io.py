import json
import typing as t
import io


from . import flat


def dump_shape(esum: flat.Esum, vertices: t.Sequence[flat.BoundsCross], f):
    json.dump(
        {
            "esum": [
                [
                    {
                        "p1": hs.p1._asdict(),
                        "p2": hs.p2._asdict(),
                        "type": type(hs).__name__,
                    }
                    for hs in term
                ]
                for term in esum.terms
            ],
            "vertices": [v.point._asdict() for v in vertices],
        },
        f,
        indent=2,
    )


def dumps_shape(esum: flat.Esum, vertices: t.Sequence[flat.BoundsCross]):
    buf = io.StringIO()
    dump_shape(esum, vertices, buf)
    buf.seek(0)
    return buf.read()
