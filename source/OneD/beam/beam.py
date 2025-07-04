"""
The 2D beam element from Chapter 5

There is an error in the 2nd edition (Elsevier, 2014)
in (5.14) correctly: N3 = 1/4 * (2 + 3 * ksi - ksi**3)
in (5.20) correctly: N3" = -3/2 * ksi

This is a 2D beam element with two nodes in the x-y plane.
The formulation results correct displacements, but the internal actions are poorly approximated.
This is a simple linear beam element, not accounting for shear deformation.

"""

from dataclasses import dataclass
from typing import Tuple, Dict

import numpy as np
import matplotlib.pyplot as plt

from source.utils import IDMixin
from source.node import Node
from source.OneD.model import Model



@dataclass
class BeamElement(IDMixin):

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
        super().__init__(self.__class__.__name__)  # Call the IDMixin constructor to set the ID
        if self.i.z is not None or self.j.z is not None:
            raise ValueError("BeamElement nodes must lie in the x-y plane (z-coordinate must be None).")
        if self.i.y != self.j.y:
            raise ValueError("BeamElement nodes y coordinate must be equal.")
        if self.A <= 0:
            raise ValueError("Cross-sectional area must be positive.")

    _length: float = None  # Length of the truss element, can be calculated
    _dof_indices: tuple = None  # DOF indices for the element in the model, to be set later by the model

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
    def Ke(self):
        return self.ke

    @property
    def me(self):
        """Local consistent mass matrix for the beam element."""
        a = self.a

        me = np.zeros((4, 4))
        me[0, :] = np.array([78, 22*a, 27, -13*a])
        me[1, :] = np.array([22*a, 8*a**2, 13*a, -6*a**2])
        me[2, :] = np.array([27, 13*a, 78, -22*a])
        me[3, :] = np.array([-13*a, -6*a**2, -22*a, 8*a**2])
        me *= self.ro * self.A * a / 105

        return me

    @property
    def Me(self):
        return self.me

    def _distributed_load(self, q: float) -> np.ndarray:
        """
        Calculates the load vector for a uniformly distributed load acting in the y direction on the beam element.
        Note: this element type performs really poor when non-nodal loads are applied!

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


@dataclass
class BeamModel(Model):
    """
    A model for a beam structure consisting of multiple beam elements.
    This class can be used to assemble the global stiffness matrix and load vector for the entire beam structure.
    """

    nodes_: Tuple[Node, ...] = None  # Nodes in the truss model
    elements_: Tuple[Tuple[
        int, int, float, float, float, float], ...] = None  # A nested tuple. # Elements in the truss model, each defined by (node_i_id, node_j_id, A, E, ro)
    supports_: Dict[int, Tuple[int, ...]] = None  # Supports. Node ID: local dof numbers e.g. {0: (0, 1, 2)}

    # not checkd if all elements have the same number of DOF per node, but it is assumed that they do.
    ND: int = 2  # Number of DOF per node

    def __post_init__(self):
        # Convert nodes and elements to dictionaries for easy access
        # This allows for quick lookups by node ID and element ID
        self.nodes = {node.ID: node for node in self.nodes_}  # Convert nodes to a dictionary for easy access
        elements_ = tuple(
            BeamElement(i=self.nodes[x[0]], j=self.nodes[x[1]], A=x[2], I=x[3], E=x[4], ro=x[5]) for x in self.elements_)
        self.elements = {x.ID: x for x in elements_}  # Convert elements to a dictionary for easy access
        self.supports = self.supports_ if self.supports_ is not None else tuple()  # Supports, a tuple of (node_id, direction)

        # set the DOF indices for each element
        self.elements = self.set_element_dof_indices()

    def plot_model(self, u: np.ndarray):
        """Plots the beam model: original and deformed shape."""
        # Plot the original beam structure
        for element in self.elements.values():
            x = [element.i.x, element.j.x]
            y = [element.i.y, element.j.y]
            plt.plot(x, y, 'b-', label='Original Beam')
            for node in self.nodes.values():
                plt.plot(node.x, node.y, 'bo')

        # Plot the deformed shape
        if u is not None:
            for element in self.elements.values():
                xs = np.linspace(element.i.x, element.j.x, 20)
                ys = []
                for x in xs:
                    ksi = (x - element.i.x) / element.length * 2 - 1  # Normalize ksi to [-1, 1]
                    # Calculate the deflection at this point
                    ys.append(element.base_functions(ksi) @ u[element.dof_indices])
                plt.plot(xs, ys, 'r--', label='Deformed Beam')
            # Plot the nodes
            displ = u[::2]
            for node, _u in zip(self.nodes.values(), displ):
                plt.plot(node.x, node.y + _u, 'ro')

            # adding the displacement values to the nodes
            # for node, _u in zip(self.nodes.values(), displ):
            #     plt.text(node.x, node.y + _u, f'{_u:.4g}', rotation=90)

        plt.xlabel('X (m)')
        plt.ylabel('Y (m)')
        plt.title('Beam Model: Original and Deformed Shape')
        plt.axhline(0, color='black', lw=0.5, ls='--')
        plt.axvline(0, color='black', lw=0.5, ls='--')
        plt.grid()
        # plt.axis('equal')
        plt.show()