"""
The 2D beam element from Chapter 5,
worked example 5.4

There is an error in the 2nd edition (Elsevier, 2014)
in (5.14) correctly: N3 = 1/4 * (2 + 3 * ksi - ksi**3)
in (5.20) correctly: N3" = -3/2 * ksi
"""

from dataclasses import dataclass

import numpy as np
import matplotlib.pyplot as plt

from source.node import Node


@dataclass
class BeamElement:

    """
    A 2D beam element with two nodes in the x-y plane.
    In this example there is no rotation of the element, so the local x-axis is aligned with the global x-axis.
    """

    i: Node  # MUST lie in the x-y plane
    j: Node  # MUST lie in the x-y plane
    A: float  # Cross-sectional area
    I: float  # Cross-section second moment of inertia
    E: float = 1.0  # Young's modulus
    ro: float = 1.0  # Density

    def __post_init__(self):
        if self.i.z is not None or self.j.z is not None:
            raise ValueError("BeamElement nodes must lie in the x-y plane (z-coordinate must be None).")
        if self.i.y != self.j.y:
            raise ValueError("BeamElement nodes y coordinate must be equal.")
        if self.A <= 0:
            raise ValueError("Cross-sectional area must be positive.")

    @property
    def length(self):
        return self.i.distance(self.j)

    @property
    def a(self):
        """Half Length of the beam element."""
        return self.length / 2

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

    def _distributed_load(self, q: float) -> np.ndarray:
        """
        Calculates the load vector for a uniformly distributed load acting in the y direction on the beam element.

        :param q: load intensity (force per unit length).
        :return: Load vector (4x1).
        """
        length_ = self.length
        
        f_e = np.array([
            q * length_ / 2,
            q * length_ ** 2 / 12,
            q * length_ / 2,
            -q * length_ ** 2 / 12
        ])
        return f_e

    def _nodal_load(self, F1: float, M1: float, F2: float, M2: float) -> np.ndarray:
        """
        Load vector for nodal forces and moments at the two nodes of the beam element.

        :param F1: Force, in y direction, at the first node.
        :param M1: Moment at the first node.
        :param F2: Force, in y direction, at the second node.
        :param M2: Moment at the second node.
        :return: Load vector (4x1).
        """
        f_e = np.array([F1, M1, F2, M2])
        return f_e

    def _gravity_load(self, g: float) -> np.ndarray:
        """
        Calculates the load vector for a uniform gravitational load acting in the y direction on the beam element.

        :param g: Gravitational acceleration (m/s^2).
        :return: Load vector (4x1).
        """
        f_e = self._distributed_load(self.ro * self.A * g)
        return f_e

    def load_vector(self, q: float = None, F1: float = None, M1: float = None, F2: float = None, M2: float = None, g: float = None) -> np.ndarray:
        """
        Calculates the load vector for the beam element.

        :param q: Uniformly distributed load (force per unit length) in the y direction.
        :param F1: Force at the first node in the y direction.
        :param M1: Moment at the first node.
        :param F2: Force at the second node in the y direction.
        :param M2: Moment at the second node.
        :param g: Gravitational acceleration (m/s^2).
        :return: Load vector (4x1).
        """
        # Initialize the load vector
        f_e = np.zeros(4)

        # If a uniformly distributed load is specified, add it to the load vector
        if q is not None:
            f_e += self._distributed_load(q)

        # If any of the nodal loads are specified, add them to the load vector
        nodal_load = []
        for attr in ('F1', 'M1', 'F2', 'M2'):
            if locals()[attr] is not None:
                nodal_load.append(float(locals()[attr]))
            else:
                nodal_load.append(0.0)
        f_e += self._nodal_load(*nodal_load)

        # gravity load
        if g is not None:
            f_e += self._gravity_load(g)

        return f_e

    def plot_deflections(self, xs: np.ndarray, u: np.ndarray):
        """
        Plots the deflection alon the x axis at the positions given in xs.

        :param xs: Local coordinates along the beam element.
        :param u: Displacements vector for the beam element.
        """

        #c calculate the y values for the xs positions
        ys = []
        for x in xs:
            # the ksi value for this x position
            ksi = (x / self.a)
            # the deflection at this point
            ys.append(self.base_functions(ksi) @ u)

        # plot the elasic line
        plt.plot(xs, ys, label='Deflection')

        # Plot the nodes
        plt.plot(xs, ys, 'ro', label='Nodes')
        # add the deflection to all nodes, vertically aligned over the node
        for x, y in zip(xs, ys):
            plt.text(x, y, '{:.2g}'.format(y), rotation=90)

        plt.xlabel('x (m)')
        plt.ylabel('Deflection (m)')
        plt.title('Beam Element Deflection')
        plt.axhline(0, color='black', lw=0.5, ls='--')
        plt.axvline(0, color='black', lw=0.5, ls='--')
        plt.legend()
        plt.grid()
        plt.show()
