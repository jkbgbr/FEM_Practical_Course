"""
The 3D beam-column element from Chapter 6.3

There is an error in the 2nd edition (Elsevier, 2014)
in (5.14) correctly: N3 = 1/4 * (2 + 3 * ksi - ksi**3)
in (5.20) correctly: N3" = -3/2 * ksi

This is a 3D euler-bernoulli beam element with two nodes in the 3D space.
The formulation results correct displacements, but the internal actions are poorly approximated.
This is a simple linear beam element, not accounting for shear deformation.

"""
import pprint
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

    _length: float = None  # Length of the truss element, can be calculated
    _dof_indices: tuple = None  # DOF indices for the element in the model, to be set later by the model

    def __post_init__(self):
        super().__init__(self.__class__.__name__)  # Call the IDMixin constructor to set the ID
        if self.i.z is None or self.j.z is None:
            raise ValueError("BeamElement nodes must be in 3D.")

        # setting the number of degrees of freedom for the truss element
        self.ND = 6

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
    def direction_vector(self) -> np.array:
        """The direction vector points from node i to node j."""
        return self.j.coords - self.i.coords

    @property
    def transformation_matrix(self) -> np.array:
        """
        Transformation matrix for a 3D element.
        This is a 12x12 matrix that transforms the global stuff to locals.

        Usage:
        Glob = np.array((1, 1, 1, 1, 3, 5))  # global displacements or forces
        T = element.transformation_matrix
        loc = T @ Glob  # in the local coordinate system

        :return: Transformation matrix for the truss element.
        """
        e1 = self.direction_vector / self.length

        # Handle the special case where the element is parallel to the global Z-axis
        # We use a different auxiliary vector in this case.
        if np.allclose(np.abs(e1), [0, 0, 1]):
            # Element is vertical, use global Y-axis as auxiliary vector
            aux_vec = np.array([0, 1, 0])
            e3 = np.cross(e1, aux_vec)
            e3 /= np.linalg.norm(e3)
            e2 = np.cross(e3, e1)
        else:
            # Standard case, use global Z-axis as auxiliary vector
            aux_vec = np.array([0, 0, 1])
            e2 = np.cross(aux_vec, e1)
            e2 /= np.linalg.norm(e2)
            e3 = np.cross(e1, e2)

        # 2. Create the 3x3 rotation matrix R
        R = np.vstack([e1, e2, e3])

        # 3. Assemble the 12x12 transformation matrix T
        T = np.zeros((12, 12))
        for i in range(4):
            T[i*3:(i+1)*3, i*3:(i+1)*3] = R

        return T

    @property
    def ke(self):
        """Local stiffness matrix for the beam element."""
        L = 2 * self.a
        EA = self.A * self.E
        EIy = self.E * self.Iy
        EIz = self.E * self.Iz
        GJ = self.G * self.J

        lila = EA / L
        green_1 = 12 * EIz / L ** 3
        green_2 = 6 * EIz / L ** 2
        green_3 = 4 * EIz / L
        green_4 = 2 * EIz / L
        blue_1 = 12 * EIy / L ** 3
        blue_2 = 6 * EIy / L ** 2
        blue_3 = 4 * EIy / L
        blue_4 = 2 * EIy / L
        gray = GJ / L

        ke = np.zeros((12, 12))
        ke[0, :] = np.array([lila, 0, 0, 0, 0, 0, -lila, 0, 0, 0, 0, 0])
        ke[1, :] = np.array([0, green_1, 0, 0, 0, green_2, 0, -green_1, 0, 0, 0, green_2,])
        ke[2, :] = np.array([0, 0, blue_1, 0, -blue_2, 0, 0, 0, -blue_1, 0, -blue_2, 0])
        ke[3, :] = np.array([0, 0, 0, gray, 0, 0, 0, 0, 0, -gray, 0, 0])
        ke[4, :] = np.array([0, 0, 0, 0, blue_3, 0, 0, 0, blue_2, 0, blue_4, 0])
        ke[5, :] = np.array([0, 0, 0, 0, 0, green_3, 0, -green_2, 0, 0, 0, green_4])
        ke[6, :] = np.array([0, 0, 0, 0, 0, 0, lila, 0, 0, 0, 0, 0])
        ke[7, :] = np.array([0, 0, 0, 0, 0, 0, 0, green_1, 0, 0, 0, -green_2])
        ke[8, :] = np.array([0, 0, 0, 0, 0, 0, 0, 0, blue_1, 0, blue_2, 0])
        ke[9, :] = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, gray, 0, 0])
        ke[10, :] = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, blue_3, 0])
        ke[11, :] = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, green_3])

        # making it symmetric
        ke = ke + ke.T - np.diag(np.diag(ke))

        return ke

    @property
    def me(self):
        """Local mass matrix for the beam element."""

        L = self.length
        rx = self.J / self.A

        me = np.zeros((12, 12))
        me[0, :] = np.array([1/3, 0, 0, 0, 0, 0, 1/6, 0, 0, 0, 0, 0])
        me[1, :] = np.array([0, 156/420, 0, 0, 0, 22 * L / 420, 0, 54 / 420, 0, 0, 0, -13 * L / 420,])
        me[2, :] = np.array([0, 0, 156/420, 0, -22 * L / 420, 0, 0, 0, 54 / 420, 0, 13 * L / 420, 0])
        me[3, :] = np.array([0, 0, 0, rx / 3, 0, 0, 0, 0, 0, rx / 6, 0, 0])
        me[4, :] = np.array([0, 0, 0, 0, 4 * L ** 2 / 420, 0, 0, 0, -13 * L / 420, 0, -3 * L ** 2 / 420, 0])
        me[5, :] = np.array([0, 0, 0, 0, 0, 4 * L ** 2 / 420, 0, 13 * L / 420, 0, 0, 0, -3 * L ** 2 / 420])
        me[6, :] = np.array([0, 0, 0, 0, 0, 0, 1/3, 0, 0, 0, 0, 0])
        me[7, :] = np.array([0, 0, 0, 0, 0, 0, 0, 156 / 420, 0, 0, 0, -22 * L / 420])
        me[8, :] = np.array([0, 0, 0, 0, 0, 0, 0, 0, 156 / 420, 0, 22 * L, 0])
        me[9, :] = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, rx / 3, 0, 0])
        me[10, :] = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4 * L ** 2 / 420, 0])
        me[11, :] = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4 * L ** 2 / 420])

        me *= self.ro * self.A * L

        # making it symmetric
        me = me + me.T - np.diag(np.diag(me))

        return me

    @property
    def Ke(self):
        """ Global stiffness matrix."""
        return self.lokal_to_global(self.ke)

    @property
    def Me(self):
        """ Global mass matrix."""
        return self.lokal_to_global(self.me)

    def lokal_to_global(self, array: np.array):
        """
        Convert a local array to a global array using the transformation matrix.

        :param array: Local array (e.g., displacements or forces).
        :return: Global array.
        """
        _T = self.transformation_matrix
        if array.ndim == 1:
            return _T.T @ array
        elif array.ndim == 2:
            return _T.T @ array @ _T
        else:
            raise ValueError("Array must be 1D or 2D.")


@dataclass
class SpatialFrameModel(Model):
    """
    A model for a spatial frame structure consisting of multiple beam elements.
    This class can be used to assemble the global stiffness matrix and load vector for the entire beam structure.
    """

    nodes_: Tuple[Node, ...] = None  # Nodes in the truss model
    elements_: Tuple[Tuple[
        int, int, float, float, float, float, float, float, float], ...] = None  # A nested tuple. # Elements in the truss model, each defined by (node_i_id, node_j_id, A, E, ro)
    supports_: Dict[int, Tuple[int, ...]] = None  # Supports. Node ID: local dof numbers e.g. {0: (0, 1, 2)}

    # not checkd if all elements have the same number of DOF per node, but it is assumed that they do.
    ND: int = 6  # Number of DOF per node

    def __post_init__(self):
        # Convert nodes and elements to dictionaries for easy access
        # This allows for quick lookups by node ID and element ID
        self.nodes = {node.ID: node for node in self.nodes_}  # Convert nodes to a dictionary for easy access
        elements_ = tuple(
            SpatialFrameElement(i=self.nodes[x[0]], j=self.nodes[x[1]], A=x[2], Iy=x[3], Iz=x[4], J=x[5], E=x[6], ro=x[7], nu=x[8]) for x in self.elements_)
        self.elements = {x.ID: x for x in elements_}  # Convert elements to a dictionary for easy access
        self.supports = self.supports_ if self.supports_ is not None else tuple()  # Supports, a tuple of (node_id, direction)

        # set the DOF indices for each element
        self.elements = self.set_element_dof_indices()

    def member_forces(self, u: np.array) -> np.array:
        """
        Calculate the member internal actions in the elements.

        :param u: Global displacement vector.
        :return: Internal actions in a dict.
        """
        forces = {}

        # Iterate over each element and calculate the member force
        for i, element in self.elements.items():
            Du = u[element.dof_indices]  # global displacements of the nodes in the element
            _T = element.transformation_matrix
            # Transform the global displacements to local displacements
            du = _T @ Du
            # Calculate the member force using the local stiffness matrix.
            nodal_forces = element.ke @ du  # Global stiffness matrix times the displacements

            res = {element.i.ID: nodal_forces[:element.ND],
                   element.j.ID: nodal_forces[element.ND:]}

            forces[i] = res  # Store the force at node i (the second node in the element)

        return forces

    def plot_frame(self, u: np.array = None, disp_factor: float = None):
        """
        Plot the structure with optional displacements.

        :param u: Global displacement vector. If provided, the truss will be plotted with displacements.
        """
        import matplotlib.pyplot as plt
        fig = plt.figure()

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

        plt.show()


if __name__ == '__main__':  # pragma: no cover

    n1 = Node(1, 1, 0)
    n2 = Node(-1, 1, 0)
    n3 = Node(-1, -1, 0)
    n4 = Node(1, -1, 0)
    n5 = Node(0, 0, 1)
    
    model = SpatialFrameModel(
        nodes_=(n1, n2, n3, n4, n5),
        elements_=(
            (n1.ID, n5.ID, 1, 1, 1, 1, 1, 1, 0.3),
            (n2.ID, n5.ID, 1, 1, 1, 1, 1, 1, 0.3),
            (n3.ID, n5.ID, 1, 1, 1, 1, 1, 1, 0.3),
            (n4.ID, n5.ID, 1, 1, 1, 1, 1, 1, 0.3),
        ),
        supports_={
            n1.ID: (0, 1, 2, ),
            n2.ID: (0, 1, 2, ),
            n3.ID: (0, 1, 2, ),
            n4.ID: (0, 1, 2, ),
        }
    )

    _F = np.zeros(model.ND * len(model.nodes))  # No external forces
    _F[model.elements[0].dof_indices[-6]] = 400  # Apply a load of -1000 N at node 5 in the -Z direction
    _F[model.elements[0].dof_indices[-4]] = -1000  # Apply a load of -1000 N at node 5 in the -Z direction
    u, r = model.solve(_F)

    print(u)

    pprint.pprint(model.member_forces(u))

    exit()
    model.plot_frame(u)
