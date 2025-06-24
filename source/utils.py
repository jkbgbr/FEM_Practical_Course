import numpy as np
from typing import Tuple


def assemble_global_K(ND: int, nodes: np.array, elements: np.array,) -> np.array:
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


def apply_boundary_conditions(ND: int, supports: tuple, K: np.array, F: np.array) -> Tuple[np.array, np.array]:
    """
    Apply boundary conditions to the global stiffness matrix and force vector.
    This method modifies the global stiffness matrix and force vector in place.

    :param ND:
    :param supports:
    :param F: Global force vector.
    :param K: stiffness matrix.
    :return: Modified global stiffness matrix and force vector.
    """

    # # dofs will be removed from the stiffness matrix and force vector
    # # this is done by first reverse sorting the supports by node_id and direction to avoid problems with indices changing after deletion
    _supports = sorted(supports, key=lambda x: (x[0], x[1]), reverse=True)

    for node_id, direction in _supports:
        dof_index = ND * node_id + {'x': 0, 'y': 1, 'z': 2}[direction]

        # Apply boundary conditions using the penalty method
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
