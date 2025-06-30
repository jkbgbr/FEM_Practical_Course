"""
2D Quadrilateral elements

"""
import pprint
from dataclasses import dataclass
from typing import Tuple, Dict

import numpy as np

from source.utils import IDMixin
from source.node import Node


@dataclass
class RM2DPlate(IDMixin):

    """
    2D 4 node isoparametric Reissner-Mindlin plate in the x-y plane
    3 DOFs each node:
    - w: deflection in the z direction
    - thex: rotation about x
    - they: rotation about y

    Node order: wi, thexi, theyi with i=1, 2, 3, 4

    """

    i: Node
    j: Node
    k: Node
    l: Node
    t: float  # thickness
    E: float  # Youngs module
    nu: float  # Poisson ratio

    def __post_init__(self):
        super().__init__(self.__class__.__name__)  # Call the IDMixin constructor to set the ID
        self.ND = 3  # w, thex, they
        self.nodes = 4

    def _N(self, xi: float, eta: float) -> np.array:
        """shape functions"""
        assert -1 <= xi <= 1, "-1 <= xi <= 1 required"
        assert -1 <= eta <= 1, "-1 <= eta <= 1 required"

        return np.array([
            0.25 * (1 - xi) * (1 - eta),
            0.25 * (1 + xi) * (1 - eta),
            0.25 * (1 + xi) * (1 + eta),
            0.25 * (1 - xi) * (1 + eta),
        ])

    def _dNdxi(self, xi: float, eta: float) -> np.array:
        """derivative of the shape functions by xi"""
        assert -1 <= xi <= 1, "-1 <= xi <= 1 required"
        assert -1 <= eta <= 1, "-1 <= eta <= 1 required"

        return np.array([
            -(1 - eta) / 4,
            (1 - eta) / 4,
            (1 + eta) / 4,
            -(1 + eta) / 4,
        ])

    def _dNdeta(self, xi: float, eta: float) -> np.array:
        """derivative of the shape functions by eta"""
        assert -1 <= xi <= 1, "-1 <= xi <= 1 required"
        assert -1 <= eta <= 1, "-1 <= eta <= 1 required"

        return np.array([
            -(1 - xi) / 4,
            -(1 + xi) / 4,
            (1 + xi) / 4,
            (1 - xi) / 4,
        ])

    def N(self, xi: float, eta: float) -> np.array:
        """shape function matrix"""
        _N = self._N(xi, eta)  # the shape functions

        # preparing the return matrix
        _ret = np.zeros([self.ND, self.ND * self.nodes])

        # filling the matrix
        for i in range(self.nodes):
            for j in range(self.ND):
                _ret[j, j + self.ND * i] = _N[i]

        return _ret

    def B(self, xi: float, eta: float) -> np.array:
        """The strain matrix, composed of the partial derivatives of the shape functions"""
        _ret = np.zeros([self.ND])


@dataclass
class PlaneQuadModel:

    nodes_: Tuple[Node, ...] = None  # Nodes in the model
    elements_: Tuple[Tuple[
        int, int, int, int, float, float, float], ...] = None  # A nested tuple. For each element four nodes and the thickness.
    supports_: Dict[int, Tuple[int, ...]] = None  # Supports. Node ID: local dof numbers e.g. {0: (0, 1, 2)}

    ND: int = 3  # DOF per node

    def __post_init__(self):
        # Convert nodes and elements to dictionaries for easy access
        # This allows for quick lookups by node ID and element ID
        self.nodes = {node.ID: node for node in self.nodes_}  # Convert nodes to a dictionary for easy access
        elements_ = tuple(
            RM2DPlate(i=self.nodes[x[0]], j=self.nodes[x[1]], k=self.nodes[x[2]], l=self.nodes[x[3]], t=x[4], E=x[5], nu=x[6]) for x in self.elements_)
        self.elements = {x.ID: x for x in elements_}  # Convert elements to a dictionary for easy access
        self.supports = self.supports_ if self.supports_ is not None else tuple()  # Supports, a tuple of (node_id, direction)


if __name__ == '__main__':
    n1 = Node(-1, -1, 0)
    n2 = Node(1, -1, 0)
    n3 = Node(1, 1, 0)
    n4 = Node(-1, 1, 0)

    model = PlaneQuadModel(
        nodes_=(n1, n2, n3, n4),
        elements_=(
            (n1.ID, n2.ID, n3.ID, n4.ID, 1.2, 210, 0.3),
        ),
        supports_={
            n1.ID: (0, 1, 2,),
            n2.ID: (0, 1, 2,),
            n3.ID: (0, 1, 2,),
            n4.ID: (0, 1, 2,),
        }
    )

    element = model.elements[0]
    pprint.pprint(element.N(0, 0))