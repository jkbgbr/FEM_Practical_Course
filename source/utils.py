import numpy as np
from typing import Tuple


class IDMixin:
    """
    This mixin class provides a unique ID for each element and keeps track of the IDs in a class variable ID_counter.

    The unique IDs are required to identify the elements and nodes in the global stiffness matrix and force vector and
    so to be able to use the assemble_* functions.

    If you implemented a new element or node class, you must inherit from this class and call

    super().__init__(__class__.__name__)  # Call the IDMixin constructor to set the ID

    """
    ID_counter = {}  # class variable to keep track of the ID of the element and node

    def __init__(self, class_name: str):
        IDMixin.register_class(class_name)
        _id = IDMixin.ID_counter.get(class_name)  # set the ID of the element or node
        if _id is None:
            raise ValueError(f"IDMixin: Class {class_name} not found in ID_counter.")
        self.ID = _id
        IDMixin.ID_counter[class_name] += 1  # increment the ID counter for the next element or node

    @classmethod
    def register_class(cls, class_name: str):
        """
        Register a new class in the ID_counter dictionary.
        This is useful if you implement a new element or node class that should have unique IDs.

        :param class_name: Name of the class to register
        """
        if class_name not in cls.ID_counter:
            cls.ID_counter[class_name] = 0

    @classmethod
    def reset(cls):
        """
        Resets the IDs of the elements and nodes to 0.
        This is useful for testing purposes to ensure that the IDs are consistent across tests.

        :return:
        """
        cls.ID_counter = {}


def assemble_global_K(ND: int, nodes: np.array, elements: np.array, ) -> np.array:
    """
    Global stiffness matrix for the truss model.

    :return: Global stiffness matrix for the truss model.
    """
    n_dofs = ND * len(nodes)  # 3 degrees of freedom per node (x, y, z)
    K_global = np.zeros((n_dofs, n_dofs))  # quadratic, symmetric
    # Assemble the global stiffness matrix
    for _id, element in elements.items():
        K_element = element.Ke  # Global stiffness matrix for the element

        dof_indices = element.dof_indices  # Use the pre-set DOF indices for the element
        for i in range(2 * ND):
            for j in range(2 * ND):
                # add the i,j element of the local stiffness matrix to the element of the global stiffness matrix defined by the global dof indices.
                K_global[dof_indices[i], dof_indices[j]] += K_element[i, j]

    return K_global


def apply_boundary_conditions(ND: int, supports: dict, K: np.array, F: np.array) -> Tuple[np.array, np.array]:
    """
    Apply boundary conditions to the global stiffness matrix and force vector.
    This method modifies the global stiffness matrix and force vector in place.

    Supports: a dict with the node ID as key and a list of local DOFs as value.
    The local DOFs are the indices of the degrees of freedom that are constrained and these depend on the element.

    :param ND:
    :param supports: Dictionary of supports where keys are node IDs and values are lists of local DOFs.
    :param F: Global force vector.
    :param K: stiffness matrix.
    :return: Modified global stiffness matrix and force vector.
    """

    # # dofs will be removed from the stiffness matrix and force vector
    # # this is done by first reverse sorting the supports by node_id and direction to avoid problems with indices changing after deletion

    # sort the supports dirct by keys in descending order
    supports = dict(sorted(supports.items(), key=lambda x: (x[0], x[1]), reverse=True))

    for node_id, local_dofs in supports.items():
        for local_dof in local_dofs:
            global_dof = ND * node_id + local_dof
            # Apply boundary conditions using the penalty method
            # Set the row and column of the stiffness matrix to zero
            K[global_dof, :] = 0
            K[:, global_dof] = 0
            # Set the diagonal element to a large value (to avoid singularity)
            # note: the value 1e20 is arbitrary, it should be large enough to avoid numerical issues - check all other
            # values in the global stiffness matrix
            K[global_dof, global_dof] = 1e20
            # Set the corresponding force to zero
            F[global_dof] = 0

    return K, F


def set_element_dof_indices(ND, elements: dict):
    """
    This is for convenience only. It will set the global dof indices for each element so it doesn't
    have to be done each time.
    Set the element DOF indices for each element.
    This is used to assemble the global stiffness matrix.
    """
    for element in elements.values():
        # the _global_ DOF indices for this element
        if ND == 2:
            element._dof_indices = tuple([ND * element.i.ID, ND * element.i.ID + 1,
                                         ND * element.j.ID, ND * element.j.ID + 1])
        else:
            element._dof_indices = tuple(
                [ND * element.i.ID, ND * element.i.ID + 1, ND * element.i.ID + 2,
                 ND * element.j.ID, ND * element.j.ID + 1, ND * element.j.ID + 2])

    return elements



def reaction_forces(K: np.array, u: np.array, f_external: np.array) -> np.array:
    """
    Calculates the reaction forces at the supports.
    The reaction forces are calculated using the formula R = K * u - F.

    :param K: Global stiffness matrix.
    :param u: The displacement vector (solution of the system after applying BCs).
    :param f_external: The original global external force vector (before applying BCs).
    :return: The vector of reaction forces. Non-zero values exist only at supported DOFs.
    """

    reactions = K @ u - f_external

    return reactions