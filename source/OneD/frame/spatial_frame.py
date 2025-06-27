"""
The 3D beam-column element from Chapter 6.3

There is an error in the 2nd edition (Elsevier, 2014)
in (5.14) correctly: N3 = 1/4 * (2 + 3 * ksi - ksi**3)
in (5.20) correctly: N3" = -3/2 * ksi

This is a 3D euler-bernoulli beam element with two nodes in the 3D space.
The formulation results correct displacements, but the internal actions are poorly approximated.
This is a simple linear beam element, not accounting for shear deformation.

"""

from dataclasses import dataclass
from typing import Tuple, Dict

import numpy as np
import matplotlib.pyplot as plt

from source.OneD.utils import IDMixin
from source.OneD.node import Node
from source.OneD.model import Model



@dataclass
class SpatialFrameElement(IDMixin):

    """
    A 3D beam-column element with two nodes.
    """

    i: Node
    j: Node
    A: float  # Cross-sectional area
    Iy: float  # Cross-section second moment of inertia
    Iz: float  # Cross-section second moment of inertia
    J: float  # Torsional constant
    E: float = 1.0  # Young's modulus
    ro: float = 1.0  # Density
    nu: float = 0.3  # Poisson's ratio

    def __post_init__(self):
        super().__init__(self.__class__.__name__)  # Call the IDMixin constructor to set the ID
        if self.i.z is None or self.j.z is None:
            raise ValueError("BeamElement nodes must be in 3D.")

    _length: float = None  # Length of the truss element, can be calculated
    _dof_indices: tuple = None  # DOF indices for the element in the model, to be set later by the model

    @property
    def G(self):
        return self.E / (2 * (1 + self.nu))  # Shear modulus, assuming isotropic material

    @property
    def length(self) -> float:
        """Calculate the length of the truss element."""
        if self._length is None:
            self._length = self.i.distance(self.j)
        return self._length

    @property
    def dof_indices(self):
        return self._dof_indices

    @property
    def a(self):
        """Half Length of the beam element."""
        return self.length / 2

    @property
    def ke(self):
        """Local stiffness matrix for the beam element."""
        a = self.a

        EA = self.A * self.E
        EIy = self.E * self.Iy
        EIz = self.E * self.Iz
        GJ = self.G * self.J

        lila = EA / self.length
        green_1 = 3 * EIz / (2 * a ** 3)
        green_2 = 2 * EIz / a
        blue_1 = 3 * EIy / (2 * a ** 3)
        blue_2 = 2 * EIy / a
        gray = GJ / (2 * a)

        ke = np.zeros((12, 12))
        ke[0, :] = np.array([lila, 0, 0, 0, 0, 0,  -lila, 0, 0, 0, 0, 0])
        ke[1, :] = np.array([0, green_1, 0, 0, 0, green_1, 0, -green_1, 0, 0, 0, green_1,])
        ke[2, :] = np.array([0, 0, blue_1, 0, blue_1, 0, 0, 0, -blue_1, 0, -blue_1, 0])
        ke[3, :] = np.array([0, 0, 0, gray, 0, 0, 0, 0, 0, -gray, 0, 0])
        ke[4, :] = np.array([0, 0, blue_1, 0, blue_2, 0, 0, 0, blue_1, 0, blue_2 / 2, 0])
        ke[5, :] = np.array([0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0])
        ke[6, :] = np.array([0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0])
        ke[7, :] = np.array([0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0])
        ke[8, :] = np.array([0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0])
        ke[9, :] = np.array([0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0])
        ke[10, :] = np.array([0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0])
        ke[11, :] = np.array([0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0])

        return ke

    @property
    def Ke(self):
        return self.ke
