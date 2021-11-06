import typing as t
import abc
from dataclasses import dataclass

import numpy as np


Value = float


@dataclass
class AffineTransform:
    """
    Source: https://en.wikipedia.org/wiki/Affine_transformation

    y = Ax + b
    """

    A: np.ndarray
    b: np.ndarray

    def compose(self, inner: "AffineTransform") -> "AffineTransform":
        """
        y = Ax + b
        z = Cy + d = C(Ax + b) + d = CAx + Cb + d = (CA)x + (Cb + d)
        """
        # TODO: rename "inner" to "outer" because it's the other way round
        return AffineTransform(
            A=inner.A @ self.A,
            b=inner.A @ self.b + inner.b,
        )

    @classmethod
    def identity(cls):
        return AffineTransform(np.eye(2), np.zeros(2))


class Shape(abc.ABC):
    @abc.abstractmethod
    def points(self) -> np.ndarray:
        """Array of shape [2 x n_points], where:
        - the 0 row are X coords
        - the 1 row are Y coords
        """
        pass


class Node(abc.ABC):
    @abc.abstractmethod
    def iter_shapes(
        self, transform: AffineTransform
    ) -> t.Iterable[t.Tuple[AffineTransform, Shape]]:
        pass


# ---- shapes ----


@dataclass
class Circle(Node, Shape):
    radius: Value

    def iter_shapes(self, transform):
        yield transform, self

    # def points(self):
    #     pass


@dataclass
class Rectangle(Node, Shape):
    width: Value
    height: Value

    def iter_shapes(self, transform):
        yield transform, self

    def points(self):
        return np.array(
            [
                [0, self.width, self.width, 0],
                [0, 0, self.height, self.height],
            ]
        )


# ---- transformations ----


@dataclass
class Translation(Node):
    x: Value
    y: Value
    child: Node

    def iter_shapes(self, transform: AffineTransform):
        new_transform = transform.compose(
            AffineTransform(np.eye(2), np.array([self.x, self.y]))
        )
        yield from self.child.iter_shapes(new_transform)


@dataclass
class Rotation(Node):
    radians: Value
    child: Node

    def iter_shapes(self, transform):
        new_transform = transform.compose(
            AffineTransform(
                np.array(
                    [
                        [np.cos(self.radians), -np.sin(self.radians)],
                        [np.sin(self.radians), np.cos(self.radians)],
                    ]
                ),
                np.zeros(2),
            )
        )
        yield from self.child.iter_shapes(new_transform)


@dataclass
class Scaling(Node):
    ratio_x: Value
    ratio_y: Value
    child: Node

    def iter_shapes(self, transform):
        new_transform = transform.compose(
            AffineTransform(
                np.array(
                    [
                        [self.ratio_x, 0],
                        [0, self.ratio_y],
                    ]
                ),
                np.zeros(2),
            )
        )

        yield from self.child.iter_shapes(new_transform)


# ---- grouping ----


@dataclass
class Group(Node):
    children: t.Tuple[Node, ...]

    def iter_shapes(self, transform):
        for child in self.children:
            yield from self.child.iter_shapes(transform)


# ---- operators ----


@dataclass
class Union(Node):
    operands: t.Tuple[Node, ...]

    def iter_shapes(self, transform):
        for operand in self.operands:
            yield from self.child.iter_shapes(transform)


@dataclass
class Product(Node):
    operands: t.Tuple[Node, ...]

    def iter_shapes(self, transform):
        for operand in self.operands:
            yield from self.child.iter_shapes(transform)


@dataclass
class Difference(Node):
    operands: t.Tuple[Node, ...]

    def iter_shapes(self, transform):
        for operand in self.operands:
            yield from self.child.iter_shapes(transform)


# ---- functions ----


def iter_shapes(root: Node):
    yield from root.iter_shapes(AffineTransform.identity())
