import io
import json
import typing as t

from . import flat


def dump_shape(esum: flat.Esum, vertices: t.Sequence[flat.X], f):
    json.dump(
        {
            "esum": [
                [
                    {
                        "p1": hs.p1._asdict(),
                        "p2": hs.p2._asdict(),
                        "type": type(hs).__name__,
                    }
                    for hs in term.hses
                ]
                for term in esum.eterms
            ],
            "vertices": [v.point._asdict() for v in vertices],
        },
        f,
        indent=2,
    )


def dumps_shape(esum: flat.Esum, vertices: t.Sequence[flat.X]):
    buf = io.StringIO()
    dump_shape(esum, vertices, buf)
    buf.seek(0)
    return buf.read()
