from dataclasses import dataclass, field
from typing import Tuple

import numpy as np

from source.node import Node


@dataclass
class TrussElement:
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

    ID: int = field(init=False, default=0)  # class variable to keep track of the ID of the truss element
    ND: int = field(init=False, default=3)  # Number of degrees of freedom per node, default is 3 for 3D nodes

    def __post_init__(self):
        """Post-initialization to ensure nodes are valid."""
        if not isinstance(self.i, Node) or not isinstance(self.j, Node):
            raise TypeError("i and j must be instances of Node")
        if self.i == self.j:
            raise ValueError("Nodes i and j must be different")
        self.ID = TrussElement.ID
        TrussElement.ID += 1  # Increment the class variable ID

        # setting the number of degrees of freedom for the truss element
        TrussElement.ND = len(self.i.coords)

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
        Mass matrix of the truss element.
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

    @property
    def transformation_matrix(self) -> np.array:
        """
        Transformation matrix for the truss element.
        This is a 2x6 matrix that transforms the global displacements or forces to locals.

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


@dataclass
class TrussModel:
    """
    A model for a truss structure, containing multiple truss elements.
    """
    nodes_: Tuple[Node, ...] = None  # Nodes in the truss model
    elements_: Tuple[Tuple[
        int, int, float, float, float], ...] = None  # A nested tuple. # Elements in the truss model, each defined by (node_i_id, node_j_id, A, E, ro)
    supports_: Tuple[Tuple[int, str], ...] = None  # Supports. Node ID, direction ('x', 'y', 'z')
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
        self._set_element_dof_indices()

    def _set_element_dof_indices(self):
        """
        This is for convenience only. It will set the global dof indices for each element so it doesn't
        have to be done each time.
        Set the element DOF indices for each element.
        This is used to assemble the global stiffness matrix.
        """
        for element in self.elements.values():
            # the _global_ DOF indices for this element
            if self.ND == 2:
                element._dof_indices = tuple([self.ND * element.i.ID, self.ND * element.i.ID + 1,
                                             self.ND * element.j.ID, self.ND * element.j.ID + 1])
            else:
                element._dof_indices = tuple(
                    [self.ND * element.i.ID, self.ND * element.i.ID + 1, self.ND * element.i.ID + 2,
                     self.ND * element.j.ID, self.ND * element.j.ID + 1, self.ND * element.j.ID + 2])

    @property
    def K(self) -> np.array:
        """
        Global stiffness matrix for the truss model.

        :return: Global stiffness matrix for the truss model.
        """
        n_dofs = self.ND * len(self.nodes)  # 3 degrees of freedom per node (x, y, z)
        K_global = np.zeros((n_dofs, n_dofs))  # quadratic, symmetric
        # Assemble the global stiffness matrix
        for _id, element in self.elements.items():
            K_element = element.Ke  # Global stiffness matrix for the element

            dof_indices = element.dof_indices  # Use the pre-set DOF indices for the element
            for i in range(2 * self.ND):
                for j in range(2 * self.ND):
                    # add the i,j element of the local stiffness matrix to the element of the global stiffness matrix defined by the global dof indices.
                    K_global[dof_indices[i], dof_indices[j]] += K_element[i, j]

        return K_global

    def apply_boundary_conditions(self, F: np.array) -> Tuple[np.array, np.array]:
        """
        Apply boundary conditions to the global stiffness matrix and force vector.
        This method modifies the global stiffness matrix and force vector in place.

        :param F: Global force vector.
        :return: Modified global stiffness matrix and force vector.
        """
        K = self.K

        # # dofs will be removed from the stiffness matrix and force vector
        # # this is done by first reverse sorting the supports by node_id and direction to avoid problems with indices changing after deletion
        _supports = sorted(self.supports, key=lambda x: (x[0], x[1]), reverse=True)

        for node_id, direction in _supports:
            dof_index = self.ND * node_id + {'x': 0, 'y': 1, 'z': 2}[direction]

            # # removing the dof_indexth row and column from the stiffness matrix
            # K = np.delete(K, dof_index, axis=0)  # Remove the row
            # K = np.delete(K, dof_index, axis=1)  # Remove the column
            # F = np.delete(F, dof_index)  # Remove the corresponding force

            # Alternative method to apply boundary conditions using the penalty method
            # Set the row and column of the stiffness matrix to zero
            K[dof_index, :] = 0
            K[:, dof_index] = 0
            # Set the diagonal element to a large value (to avoid singularity)
            # note: the value 1e20 is arbitrary, it should be large enough to avoid numerical issues - check all other
            # values in the global stiffness matrix
            K[dof_index, dof_index] = 1e20
            # Set the corresponding force to zero
            F[dof_index] = 0

        return K, F

    def member_forces(self, u: np.array) -> np.array:
        """
        Calculate the member forces in the truss elements based on the displacements.

        :param u: Global displacement vector.
        :return: Member forces in the truss elements.
        """
        forces = []

        # Iterate over each element and calculate the member force
        for i, element in self.elements.items():
            Du = u[list(element.dof_indices)]  # global displacements of the nodes in the element
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

    def reaction_forces(self, u_reduced: np.array, f_external: np.array) -> np.array:
        """
        Calculates the reaction forces at the supports.
        The reaction forces are calculated using the formula R = K * u - F.

        :param u_reduced: The reduced displacement vector (solution of the system after applying BCs).
        :param f_external: The original global external force vector (before applying BCs).
        :return: The vector of reaction forces. Non-zero values exist only at supported DOFs.
        """
        # 1. Reconstruct the full displacement vector from the reduced one.
        n_total_dofs = self.ND * len(self.nodes)
        u_full = np.zeros(n_total_dofs)

        # Get the indices of the supported DOFs
        supported_dofs = {self.ND * node_id + {'x': 0, 'y': 1, 'z': 2}[direction]
                          for node_id, direction in self.supports}

        # Get the indices of the free (unsupported) DOFs
        all_dofs = set(range(n_total_dofs))
        free_dofs = sorted(list(all_dofs - supported_dofs))

        # Populate the full displacement vector with the calculated displacements
        u_full[free_dofs] = u_reduced

        # 2. Calculate reaction forces: R = K_global * u_full - F_external
        # self.K is the full global stiffness matrix before applying BCs
        reactions = self.K @ u_full - f_external

        return reactions
