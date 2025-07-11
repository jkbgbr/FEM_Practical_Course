from dataclasses import dataclass, field
from typing import Tuple, Dict

import numpy as np

from source.utils import IDMixin
from source.node import Node
from source.OneD.model import Model
# from source.utils import assemble_global_K, apply_boundary_conditions, set_element_dof_indices, reaction_forces


@dataclass
class TrussElement(IDMixin):
    """
    3D Truss element with two nodes i and j, both of type Node.
    Axial direction is the local x-axis.
    The truss element is defined by its cross-sectional area (A), Young's modulus (E), density (ro).

    Loads:
    - fx: Body load in the x-direction.
    - F: Nodal load at the nodes, node i, node j.
    """

    i: Node  # Node i
    j: Node  # Node j
    A: float = 1.0  # Cross-sectional area of the truss element
    E: float = 1.0  # Young's modulus of the material
    ro: float = 1.0  # Density of the material

    _length: float = None  # Length of the truss element, can be calculated
    _dof_indices: tuple = None  # DOF indices for the element in the model, to be set later by the model

    # # class variable to keep track of the ID of the truss element
    # # NOTE: This is a class variable, so it is shared across all instances of the class. If you have multiple
    # # instances of the TrussModel, this will cause problems as the numbering will not start at 0 for each model.
    # ID_counter: ClassVar[int] = 0  # class variable to keep track of the ID of the element
    ND: int = field(init=False, default=3)  # Number of degrees of freedom per node, default is 3 for 3D nodes

    def __post_init__(self):
        """Post-initialization to ensure nodes are valid."""
        super().__init__(self.__class__.__name__)  # Call the IDMixin constructor to set the ID
        if not isinstance(self.i, Node) or not isinstance(self.j, Node):
            raise TypeError("i and j must be instances of Node")
        if self.i == self.j:
            raise ValueError("Nodes i and j must be different")

        # setting the number of degrees of freedom for the truss element
        # todo: make clear: this is the number of DOFS per node or the number of the dimensions of the space the element is in?
        self.ND = len(self.i.coords)

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
    def direction_vector(self) -> np.array:
        """The direction vector points from node i to node j."""
        return self.j.coords - self.i.coords

    def _N1(self, x) -> float:
        """The value of the shape function for node i, evaluated at x."""
        assert 0 <= x <= self.length, "x must be within the length of the truss element"
        return 1 - (x / self.length)

    def _N2(self, x) -> float:
        """The value of the shape function for node j, evaluated at x."""
        assert 0 <= x <= self.length, "x must be within the length of the truss element"
        return x / self.length

    def N(self, x: float) -> np.array:
        """Shape functions for the truss element."""
        return np.array((self._N1(x), self._N2(x)))

    @property
    def B(self) -> np.array:
        """
        Strain in the truss element.
        B = LN = d / dx * N. (Pt. 4.2.2 in the book)
        The strain is constant along the length of the truss element.
        """
        return np.array((-1 / self.length, 1 / self.length))

    @property
    def ke(self) -> np.array:
        """
        Stiffness matrix of the truss element.
        (4.15) in the book.

        This is how B.T and B are multiplied
        # alternatives, if the definition is used:
        return (self.A * self.E / self.length) * (B[:, None] @ B[None, :])
        return (self.A * self.E / self.length) * np.outer(B, B)

        """
        return (self.A * self.E / self.length) * np.array(((1, -1), (-1, 1)))

    @property
    def me(self) -> np.array:
        """
        Consistent mass matrix of the truss element.
        (4.16) in the book.
        See truss.md for the derivation.
        :return:
        """
        return (self.A * self.ro * self.length / 6) * np.array(((2, 1), (1, 2)))

    @property
    def Ke(self):
        """ Global stiffness matrix for the truss element."""
        _T = self.transformation_matrix
        return _T.T @ self.ke @ _T

    @property
    def Me(self):
        """ Global stiffness matrix for the truss element."""
        _T = self.transformation_matrix
        return _T.T @ self.me @ _T

    @property
    def transformation_matrix(self) -> np.array:
        """
        Transformation matrix for a 3D element.
        This is a 2x6 matrix that transforms the global stuff to locals.

        Usage:
        Glob = np.array((1, 1, 1, 1, 3, 5))  # global displacements or forces
        T = element.transformation_matrix
        loc = T @ Glob  # in the local coordinate system

        :return: Transformation matrix for the truss element.
        """
        unit_vector = self.direction_vector / self.length

        # transformation matrix as in (4.20) in the book
        _T = np.zeros((2, 2 * self.ND))
        _T[0, 0:self.ND] = unit_vector
        _T[1, self.ND:2 * self.ND] = unit_vector

        return _T

    def _body_load(self, fx: float) -> np.array:

        """
        Distributed load for the truss element, force / length.
        :param fx: Load in the x-direction.
        :return: Load vector for the truss element.
        """
        return np.array((fx * self.length / 2, fx * self.length / 2))

    @staticmethod
    def _nodal_load(F: np.array) -> np.array:
        """
        Nodal load for the truss element.
        :param F: an array of loads at the nodes, node i, node j.
        :return: Load vector for the truss element.
        """
        return np.array(F)

    def force_vector(self, fx: float = 0.0, F: np.array = np.array((0, 0))) -> np.array:
        """
        Nodal force vector for the truss element.
        Pt. 4.2.3 (4,17) in the book.
        :param fx: Body load in the x-direction.
        :param F: Nodal load at the nodes, node i, node j.
        :return: Load vector for the truss element.
        """
        return self._body_load(fx) + self._nodal_load(F)


@dataclass
class TrussModel(Model):
    """
    A model for a truss structure, containing multiple truss elements.
    """
    nodes_: Tuple[Node, ...] = None  # Nodes in the truss model
    elements_: Tuple[Tuple[
        int, int, float, float, float], ...] = None  # A nested tuple. # Elements in the truss model, each defined by (node_i_id, node_j_id, A, E, ro)
    supports_: Dict[int, Tuple[int, ...]] = None  # Supports. Node ID: local dof numbers e.g. {0: (0, 1, 2)}

    ND: int = None

    def __post_init__(self):
        """Post-initialization to ensure nodes and elements are valid."""
        if self.nodes_ is None or len(self.nodes_) == 0:
            raise ValueError("At least one node must be defined in the truss model")
        if self.elements_ is None or len(self.elements_) == 0:
            raise ValueError("At least one element must be defined in the truss model")
        if not all(isinstance(node, Node) for node in self.nodes_):
            raise TypeError("All nodes must be instances of Node")
        if not all(isinstance(elem, tuple) and len(elem) == 5 for elem in self.elements_):
            raise TypeError("Each element must be a tuple of (node_i_id, node_j_id, A, E, ro)")

        # Convert nodes and elements to dictionaries for easy access
        # This allows for quick lookups by node ID and element ID
        self.nodes = {node.ID: node for node in self.nodes_}  # Convert nodes to a dictionary for easy access
        elements_ = tuple(
            TrussElement(i=self.nodes[x[0]], j=self.nodes[x[1]], A=x[2], E=x[3], ro=x[4]) for x in self.elements_)
        self.elements = {x.ID: x for x in elements_}  # Convert elements to a dictionary for easy access
        self.supports = self.supports_ if self.supports_ is not None else tuple()  # Supports, a tuple of (node_id, direction)

        # not checkd if all elements have the same number of DOF per node, but it is assumed that they do.
        self.ND = self.elements[0].ND  # Number of DOF per node, taken from the first element

        # set the DOF indices for each element
        self.elements = self.set_element_dof_indices()

    def member_forces(self, u: np.array) -> np.array:
        """
        Calculate the member forces in the truss elements based on the displacements.

        :param u: Global displacement vector.
        :return: Member forces in the truss elements.
        """
        forces = []

        # Iterate over each element and calculate the member force
        for i, element in self.elements.items():
            Du = u[element.dof_indices]  # global displacements of the nodes in the element
            _T = element.transformation_matrix
            # Transform the global displacements to local displacements
            du = _T @ Du
            # Calculate the member force using the local stiffness matrix.
            # This returns the nodal forces in the local coordinate system, one value for each node.
            # The nodal forces are the same value but opposite sign.
            # by convention, compression is negative.
            nodal_forces = element.ke @ du  # Global stiffness matrix times the displacements

            # If the j node is positive, the member is in tension.
            res = [float(nodal_forces[1]), '']
            if nodal_forces[1] < 0:
                res[1] = 'compression'
            elif nodal_forces[1] > 0:
                res[1] = 'tension'
            else:
                res[1] = 'no force'

            forces.append(res)  # Store the force at node i (the second node in the element)

        return forces

    def plot_truss(self, u: np.array = None, disp_factor: float = None):
        """
        Plot the truss structure with optional displacements.

        :param u: Global displacement vector. If provided, the truss will be plotted with displacements.
        """
        import matplotlib.pyplot as plt
        fig = plt.figure()

        if self.ND == 3:

            ax = fig.add_subplot(111, projection='3d')

            for element in self.elements.values():
                x = [element.i.coords[0], element.j.coords[0]]
                y = [element.i.coords[1], element.j.coords[1]]
                z = [element.i.coords[2], element.j.coords[2]]
                ax.plot(x, y, z, 'ko-')

                if u is not None:
                    if disp_factor is None:
                        disp_factor = (max(x.length for x in self.elements.values()) / 10) / max(
                            abs(x) for x in u)  # Default factor based on the longest element

                    # Apply displacements to the nodes
                    x_ = np.array([u[element.dof_indices[0]], u[element.dof_indices[self.ND + 0]]])
                    y_ = np.array([u[element.dof_indices[1]], u[element.dof_indices[self.ND + 1]]])
                    z_ = np.array([u[element.dof_indices[2]], u[element.dof_indices[self.ND + 2]]])

                    x_ = x_ * disp_factor
                    y_ = y_ * disp_factor
                    z_ = z_ * disp_factor

                    x_ = x_[0] + element.i.coords[0], x_[1] + element.j.coords[0]
                    y_ = y_[0] + element.i.coords[1], y_[1] + element.j.coords[1]
                    z_ = z_[0] + element.i.coords[2], z_[1] + element.j.coords[2]
                    ax.plot(x_, y_, z_, 'ro-')

        else:

            ax = fig.add_subplot(111)

            for element in self.elements.values():
                x = [element.i.coords[0], element.j.coords[0]]
                y = [element.i.coords[1], element.j.coords[1]]
                ax.plot(x, y, 'ko-')

                if u is not None:

                    if disp_factor is None:
                        disp_factor = (max(x.length for x in self.elements.values()) / 10) / max(
                            abs(x) for x in u)  # Default factor based on the longest element

                    # Apply displacements to the nodes
                    x_ = np.array([u[element.dof_indices[0]], u[element.dof_indices[self.ND + 0]]])
                    y_ = np.array([u[element.dof_indices[1]], u[element.dof_indices[self.ND + 1]]])

                    x_ = x_ * disp_factor
                    y_ = y_ * disp_factor

                    x_ = x_[0] + element.i.coords[0], x_[1] + element.j.coords[0]
                    y_ = y_[0] + element.i.coords[1], y_[1] + element.j.coords[1]
                    ax.plot(x_, y_, 'ro-')

        plt.show()
