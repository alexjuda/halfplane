import hyperplane.flat as hp
from hyperplane.flat import Esum, Hp, Hpc, Pt

esum1 = Esum(
    {
        frozenset(
            [
                # vertical line (|)
                Hp(
                    Pt(1, 6),
                    Pt(1, 1),
                ),
                # horizontal line (-)
                Hpc(
                    Pt(2, 2),
                    Pt(8, 2),
                ),
                # diagonal line (\)
                Hp(
                    Pt(15, 1),
                    Pt(0, 16),
                ),
                # horizontal line (-)
                Hp(
                    Pt(11, 10),
                    Pt(4, 10),
                ),
            ]
        )
    }
)

esum2 = Esum(
    {
        frozenset(
            [
                # diagonal line (/)
                Hpc(
                    Pt(8, 10),
                    Pt(4, 2),
                ),
                # diagonal line (\)
                Hp(
                    Pt(12, 2),
                    Pt(10, 10),
                ),
            ]
        )
    }
)

esum3 = esum1.intersection(esum2)

vertices = hp.find_vertices(esum3)

with open("exported.stl", "w") as f:
    hp.dump_to_stl(vertices, f)
