
import numpy as np
from typing import Tuple


class Model:

    def assemble_lumped_M(self) -> np.array:
        """
        Lumped mass matrix for the model,

        :return:
        """
        n_dofs = self.ND * len(self.nodes)
        M_global = np.zeros((n_dofs, n_dofs))  # quadratic, symmetric
        for _id, element in self.elements.items():
            M_element = element.Me
            dof_indices = element.dof_indices
            for i in range(2 * self.ND):
                M_global[dof_indices[i], dof_indices[i]] += M_element[i, i]  # Lumped mass matrix, only diagonal elements are non-zero

        return M_global

    def assemble_global_K(self) -> np.array:
        """
        Global stiffness matrix for the model.

        :return: Global stiffness matrix for the model.
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

    def apply_boundary_conditions(self, F: np.array = None) -> Tuple[np.array, np.array]:
        """
        Apply boundary conditions to the global stiffness matrix and force vector.
        This method modifies the global stiffness matrix and force vector in place.

        Supports: a dict with the node ID as key and a list of local DOFs as value.
        The local DOFs are the indices of the degrees of freedom that are constrained and these depend on the element.

        :param F: Global force vector.
        :return: Modified global stiffness matrix and force vector.
        """

        # # dofs will be removed from the stiffness matrix and force vector
        # # this is done by first reverse sorting the supports by node_id and direction to avoid problems with indices changing after deletion

        # sort the supports dirct by keys in descending order
        supports = dict(sorted(self.supports.items(), key=lambda x: (x[0], x[1]), reverse=True))
        K = self.K
        ND = self.ND

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

                # If a load vector is provided, Set the corresponding force to zero
                if F is not None:
                    F[global_dof] = 0

        return K, F

    def set_element_dof_indices(self):
        """
        Sets the global dof indices for each element so it doesn't have to be done each time.
        """
        ND = self.ND
        for element in self.elements.values():
            # the _global_ DOF indices for this element
            if ND == 2:
                element._dof_indices = list([ND * element.i.ID, ND * element.i.ID + 1,
                                              ND * element.j.ID, ND * element.j.ID + 1])
            else:
                element._dof_indices = list(
                    [ND * element.i.ID, ND * element.i.ID + 1, ND * element.i.ID + 2,
                     ND * element.j.ID, ND * element.j.ID + 1, ND * element.j.ID + 2])

        return self.elements

    def reaction_forces(self, u: np.array, f_external: np.array) -> np.array:
        """
        Calculates the reaction forces at the supports.
        The reaction forces are calculated using the formula R = K * u - F.

        :param u: The displacement vector.
        :param f_external: The original global external force vector.
        :return: The vector of reaction forces. Non-zero values exist only at supported DOFs.
        """
        reactions = self.K @ u - f_external

        return reactions

    @property
    def K(self):
        """The global stiffness matrix should be assembled only once."""
        return self.assemble_global_K()

    def solve(self, F):
        """
        Solve the system for the given load

        :param F:
        :return:
        """
        _K, _F = self.apply_boundary_conditions(F)  # Apply boundary conditions
        _u = np.linalg.solve(_K, _F)
        _re = self.reaction_forces(_u, _F)

        return _u, _re

    def solve_modal(self):
        """
        Solve the system for the modal analysis.

        :return: frequencies and modal shapes of the system.
        """
        M = self.assemble_lumped_M()
        K, _ = self.apply_boundary_conditions()
        # Solve the generalized eigenvalue problem
        eigenvalues, eigenvectors = np.linalg.eig(np.linalg.inv(M) @ K)

        # Sort eigenvalues and eigenvectors
        idx = np.argsort(eigenvalues)
        # Take the square root (eigenvals are omega^2) and covert to freq
        freqs = eigenvalues[idx] ** 0.5 / (2 * np.pi)
        shapes = eigenvectors[:, idx]

        return freqs, shapes