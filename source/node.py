from dataclasses import dataclass, field
from typing import ClassVar

import numpy as np


@dataclass
class Node:

    x: float
    y: float
    z: float = None  # Default z-coordinate for 2D nodes

    # Node ID.
    # NOTE: This is a class variable, so it is shared across all instances of the class.
    ID_counter: ClassVar[int] = 0  # class variable to keep track of the ID of the node

    def __post_init__(self):
        self.ID = Node.ID_counter
        Node.ID_counter += 1  # Increment the class variable ID

    def __eq__(self, other):
        """Check if two nodes are equal based on their id and location."""
        if not isinstance(other, Node):
            return NotImplemented
        _ret = []
        _ret.append(self.ID == other.ID)
        _ret.append(all(x == y for x, y in zip((self.x, self.y, self.z), (other.x, other.y, other.z))))
        return any(_ret)

    def __ne__(self, other):
        """Check if two nodes are not equal."""
        return not self.__eq__(other)

    def distance(self, other: 'Node') -> float:
        """Calculate the Euclidean distance to another node."""
        if self.z is None or other.z is None:
            # 2D distance
            return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2) ** 0.5

    @property
    def coords(self) -> np.array:
        """Return the coordinates of the node as a numpy array."""
        if self.z is None:
            return np.array([self.x, self.y])
        else:
            return np.array([self.x, self.y, self.z])