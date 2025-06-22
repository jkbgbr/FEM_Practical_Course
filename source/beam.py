"""
The 2D beam element from Chapter 5,
worked example 5.4

There is an error in the 2nd edition (Elsevier, 2014)
in (5.14) correctly: N3 = 1/4 * (2 + 3 * ksi - ksi**3)
in (5.20) correctly: N3" = -3/2 * ksi
"""

from dataclasses import dataclass

import numpy as np
from source.node import Node


@dataclass
class BeamElement:

    """
    A 2D beam element with two nodes in the x-y plane.
    In this example there is no rotation of the element, so the local x-axis is aligned with the global x-axis.
    """

    n1: Node  # MUST lie in the x-y plane
    n2: Node  # MUST lie in the x-y plane
    A: float  # Cross-sectional area
    I: float  # Cross-section second moment of inertia
    E: float = 1.0  # Young's modulus
    ro: float = 1.0  # Density

    def __post_init__(self):
        if self.n1.z is not None or self.n2.z is not None:
            raise ValueError("BeamElement nodes must lie in the x-y plane (z-coordinate must be None).")
        if self.n1.y != self.n2.y:
            raise ValueError("BeamElement nodes y coordinate must be equal.")
        if self.A <= 0:
            raise ValueError("Cross-sectional area must be positive.")

    @property
    def a(self):
        """Half Length of the beam element."""
        return self.n1.distance(self.n2) / 2

    def base_functions(self, ksi):
        """Base functions for the beam element."""
        a = self.a
        return np.array([
            1/4 * (2 - 3 * ksi + ksi**3),
            a/4 * (1 - ksi - ksi**2 + ksi**3),
            1/4 * (2 + 3 * ksi - ksi**3),  # in some books this is written as 1/4 * (2 + 3 * ksi + ksi**3) wich is incorrect
            a/4 * (-1 - ksi + ksi**2 + ksi**3)
        ])

    def base_function_1st_derivatives(self, ksi):
        """First derivatives of the base functions by ksi."""
        a = self.a
        return np.array([
            3/4 * (1 + ksi**2),
            a/4 * (-1 - 2 * ksi + 3 * ksi**2),
            -3/4 * (-1 + ksi**2),
            a/4 * (-1 + 2 * ksi + 3 * ksi**2)
        ])

    def base_function_2nd_derivatives(self, ksi):
        """Second derivatives of the base functions by ksi."""
        a = self.a
        return np.array([
            3/2 * ksi,
            a/2 * (-1 + 3 * ksi),
            -3/2 * ksi,  # sign error in the 2nd edition book
            a/2 * (1 + 3 * ksi),
        ])

    def B(self, ksi: float, y: float) -> np.ndarray:
        """
        B matrix for the beam element at a given ksi and deflection value.

        :param ksi: Local coordinate along the beam element, normalized between -1 and 1.
        :param y: Deflection at the given ksi.
        """
        B = -(y / self.a ** 2) * self.base_function_2nd_derivatives(ksi)
        return B

    @property
    def ke(self):
        """Local stiffness matrix for the beam element."""
        a = self.a

        ke = np.zeros((4, 4))
        ke[0, :] = np.array([3, 3*a, -3, 3*a])
        ke[1, :] = np.array([3*a, 4*a**2, -3*a, 2*a**2])
        ke[2, :] = np.array([-3, -3*a, 3, -3*a])
        ke[3, :] = np.array([3*a, 2*a**2, -3*a, 4*a**2])
        ke *= self.E * self.I / (2 * a ** 3)

        return ke

    @property
    def me(self):
        """Local mass matrix for the beam element."""
        a = self.a

        me = np.zeros((4, 4))
        me[0, :] = np.array([78, 22*a, 27, -13*a])
        me[1, :] = np.array([22*a, 8*a**2, 13*a, -6*a**2])
        me[2, :] = np.array([27, 13*a, 78, -22*a])
        me[3, :] = np.array([-13*a, -6*a**2, -22*a, 8*a**2])
        me *= self.ro * self.A * a / 105

        return me
