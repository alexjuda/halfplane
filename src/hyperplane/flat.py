import typing as t
from abc import ABC
from dataclasses import dataclass


Value = float


class Node(ABC):
    pass


# ---- shapes ----


@dataclass
class Circle(Node):
    radius: Value


@dataclass
class Rectangle(Node):
    width: Value
    height: Value


# ---- transformations ----


@dataclass
class Translation(Node):
    x: Value
    y: Value
    child: Node


@dataclass
class Rotation(Node):
    radians: Value
    child: Node


@dataclass
class Scaling(Node):
    ratio_x: Value
    ratio_y: Value
    child: Node


# ---- grouping ----


@dataclass
class Group(Node):
    children: t.Tuple[Node, ...]


# ---- operators ----


@dataclass
class Union(Node):
    operands: t.Tuple[Node, ...]


@dataclass
class Product(Node):
    operands: t.Tuple[Node, ...]


@dataclass
class Difference(Node):
    operands: t.Tuple[Node, ...]
